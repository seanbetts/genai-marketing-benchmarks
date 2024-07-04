import os
from dotenv import load_dotenv
from typing import List, Dict, Any
from datetime import datetime
import pandas as pd

# Load environment variables
load_dotenv()

from src.constants import MODELS, DATE_FORMAT, TIME_FORMAT, BASE_FOLDER, PROMPT_TEMPLATE, MAX_RETRIES
from src.api_calls import query_language_model
from src.data_processing import (
    load_questions, save_results_to_sqlite, calculate_token_cost, 
    estimate_cost, answer_check, check_table_exists_and_get_highest_round
)
from src.user_interface import select_models, select_categories, get_user_inputs, confirm_run
from src.logger import setup_logger, get_logger

def main() -> None:
    # Set up logger
    setup_logger(BASE_FOLDER)
    logger = get_logger()

    logger.info("Starting the GenAI Marketing Benchmarks script")

    # Get current date and time
    today_date: str = datetime.today().strftime(DATE_FORMAT)

    # Select models
    logger.info("Prompting user to select models")
    selected_models: List[Dict[str, Any]] = select_models(MODELS)
    logger.info(f"Selected models: {[model['name'] for model in selected_models]}")

    # Load questions
    logger.info("Loading questions from database")
    questions_df: pd.DataFrame = load_questions()
    logger.info(f"Loaded {len(questions_df)} questions from database")

    # Select categories
    categories = questions_df['Category'].unique().tolist()
    logger.info("Prompting user to select categories")
    selected_categories = select_categories(categories)
    logger.info(f"Selected categories: {selected_categories}")

    # Filter questions based on selected categories
    filtered_df = questions_df[questions_df['Category'].isin(selected_categories)]
    logger.info(f"Filtered to {len(filtered_df)} questions based on selected categories")

    # Get user inputs
    logger.info("Getting user inputs for number of questions and rounds")
    num_questions, num_rounds = get_user_inputs()
    logger.info(f"User input: {num_questions} questions, {num_rounds} rounds")

    # Calculate total available questions
    total_questions: int = len(filtered_df)

    # Calculate estimated cost
    questions_per_round = total_questions if num_questions == 'all' else min(int(num_questions), total_questions)
    estimated_cost, model_costs = estimate_cost(questions_per_round, num_rounds, selected_models)
    logger.info(f"Estimated total cost: ${estimated_cost:.3f}")

    # Confirm run
    logger.info("Asking user to confirm the run")
    if not confirm_run(estimated_cost, model_costs, num_rounds, num_questions, total_questions):
        logger.info("User aborted the run")
        print("Testing run aborted by the user.")
        return

    # Main testing loop
    for model_info in selected_models:
        logger.info(f"Starting tests for model: {model_info['name']}")

        # Check for existing rounds and get the highest round number
        highest_round: int = check_table_exists_and_get_highest_round(model_info['variant'], today_date)
        start_round: int = highest_round + 1

        for iteration in range(start_round, start_round + num_rounds):
            logger.info(f"Starting round {iteration} for {model_info['name']}")
            results: List[Dict[str, Any]] = []
            questions_to_test = filtered_df if num_questions == 'all' else filtered_df.sample(n=min(num_questions, total_questions))
            for index, question in questions_to_test.iterrows():
                logger.info(f"Processing question {index + 1}")
                # Prepare the prompt
                prompt = PROMPT_TEMPLATE.format(
                    question=question['Question'],
                    option_a=question['Option_A'],
                    option_b=question['Option_B'],
                    option_c=question['Option_C'],
                    option_d=question['Option_D']
                )
                
                # Query the model
                logger.info(f"Querying model {model_info['name']}...")
                answer, prompt_tokens, completion_tokens = query_language_model(
                    model_info['provider'],
                    model_info['variant'],
                    prompt
                )

                # Check the answer
                logger.info(f"Raw answer from model: {answer}")
                cleaned_answer, is_valid = answer_check(answer)
                logger.info(f"Cleaned answer: {cleaned_answer}, Is valid: {is_valid}")

                # If the answer is not valid, retry (you might want to limit the number of retries)
                retry_count: int = MAX_RETRIES
                while not is_valid and retry_count > 0:
                    logger.warning(f"Invalid answer, retrying. Attempts left: {retry_count}")
                    answer, prompt_tokens, completion_tokens = query_language_model(
                        model_info['provider'],
                        model_info['variant'],
                        prompt
                    )
                    logger.info(f"Raw answer from model (retry): {answer}")
                    cleaned_answer, is_valid = answer_check(answer)
                    logger.info(f"Cleaned answer (retry): {cleaned_answer}, Is valid: {is_valid}")
                    retry_count -= 1

                if not is_valid:
                    logger.error(f"Failed to get a valid answer after retries. Skipping this question.")
                    continue

                # Process the result
                is_correct: bool = cleaned_answer == question['Correct_Option']
                cost: float = calculate_token_cost(prompt_tokens, completion_tokens, model_info)

                logger.info(f"Final answer: {cleaned_answer}")
                logger.info(f"Question {index + 1} result: Correct: {is_correct}")

                # Store the result
                results.append({
                    'Round': iteration,
                    'Discipline': question['Discipline'],
                    'Category': question['Category'],
                    'Sub_Category': question.get('Sub_Category'),
                    'Question_Code': question['Question_Code'],
                    'Question': question['Question'],
                    'Correct_Option': question['Correct_Option'],
                    'Provider': model_info['provider'],
                    'Model': model_info['name'],
                    'Model_Answer': cleaned_answer,
                    'Is_Correct': is_correct,
                    'Cost': cost,
                    'Timestamp': datetime.now()
                })

            # Save results
            logger.info(f"Saving results for round {iteration }")
            results_df = pd.DataFrame(results)
            save_results_to_sqlite(results_df, model_info['variant'], BASE_FOLDER, today_date)

        logger.info(f"Completed all rounds for model: {model_info['name']}")

    logger.info("Testing completed successfully")

if __name__ == "__main__":
    main()