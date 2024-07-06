import click
from typing import List, Union, Dict, Any
from datetime import datetime
import pandas as pd
import os
import sys
from dotenv import load_dotenv

# Load environment variables at the very beginning
load_dotenv()

from src.constants import MODELS, BASE_FOLDER, DATE_FORMAT, PROMPT_TEMPLATE, MAX_RETRIES
from src.user_interface import select_models, select_categories, get_user_inputs, confirm_run
from src.data_processing import (
    load_questions, save_results_to_sqlite, calculate_token_cost, 
    estimate_cost, answer_check, check_table_exists_and_get_highest_round
)
from src.api_calls import query_language_model
from src.logger import setup_logger, get_logger

@click.command()
@click.option('--num-questions', default='all', help='Number of questions to test (or "all" for all questions)')
@click.option('--num-rounds', default=1, type=int, help='Number of rounds to run')
@click.option('--models', '-m', multiple=True, help='Models to use for testing (can be specified multiple times)')
@click.option('--categories', '-c', multiple=True, help='Categories to test (can be specified multiple times)')
@click.option('--interactive/--non-interactive', default=True, help='Run in interactive mode (default) or non-interactive mode')

def run_benchmark(num_questions: str, num_rounds: int, models: List[str], categories: List[str], interactive: bool):
    """Run the GenAI Marketing Benchmarks."""
    try:
        setup_logger(BASE_FOLDER)
        logger = get_logger()

        logger.info("Starting the GenAI Marketing Benchmarks script")

        # Check if API keys are set
        required_keys = ['OPENAI_API_KEY', 'CLAUDE_API_KEY', 'TOGETHER_API_KEY']
        missing_keys = [key for key in required_keys if not os.getenv(key)]
        if missing_keys:
            for key in missing_keys:
                logger.error(f"{key} is not set in the environment variables.")
            sys.exit(1)

        # Get current date and time
        today_date: str = datetime.today().strftime(DATE_FORMAT)

        # Load questions
        logger.info("Loading questions from database")
        questions_df: pd.DataFrame = load_questions()
        logger.info(f"Loaded {len(questions_df)} questions from database")

        if interactive:
            selected_models = select_models(MODELS)
            all_categories = questions_df['Category'].unique().tolist()
            selected_categories = select_categories(all_categories)
            num_questions, num_rounds = get_user_inputs()
        else:
            selected_models = [model for model in MODELS if model['name'] in models]
            selected_categories = list(categories)
            num_questions = num_questions if num_questions != 'all' else len(questions_df)

        if not selected_models:
            logger.error("No models selected. Exiting.")
            sys.exit(1)

        if not selected_categories:
            logger.error("No categories selected. Exiting.")
            sys.exit(1)

        logger.info(f"Selected models: {[model['name'] for model in selected_models]}")
        logger.info(f"Selected categories: {selected_categories}")
        logger.info(f"Number of questions: {num_questions}")
        logger.info(f"Number of rounds: {num_rounds}")

        # Filter questions based on selected categories
        filtered_df = questions_df[questions_df['Category'].isin(selected_categories)]

        # Calculate total available questions
        total_questions: int = len(filtered_df)

        if total_questions == 0:
            logger.error("No questions available for the selected categories. Exiting.")
            sys.exit(1)

        # Calculate estimated cost
        questions_per_round = total_questions if num_questions == 'all' else min(int(num_questions), total_questions)
        estimated_cost, model_costs = estimate_cost(questions_per_round, num_rounds, selected_models)
        logger.info(f"Estimated total cost: ${estimated_cost:.3f}")

        # Confirm run
        if interactive:
            logger.info("Asking user to confirm the run")
            if not confirm_run(estimated_cost, model_costs, num_rounds, num_questions, total_questions):
                logger.info("User aborted the run")
                print("Testing run aborted by the user.")
                return  # Use return instead of sys.exit(0)
            
        # Main testing loop
        for model_info in selected_models:
            logger.info(f"Starting tests for model: {model_info['name']}")

            # Check for existing rounds and get the highest round number
            highest_round: int = check_table_exists_and_get_highest_round(model_info['variant'], today_date)
            start_round: int = highest_round + 1

            for iteration in range(start_round, start_round + num_rounds):
                logger.info(f"Starting round {iteration} for {model_info['name']}")
                results: List[Dict[str, Any]] = []
                questions_to_test = filtered_df if num_questions == 'all' else filtered_df.sample(n=min(int(num_questions), total_questions))
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
                save_results_to_sqlite(results_df, model_info['variant'], today_date)

            logger.info(f"Completed all rounds for model: {model_info['name']}")

        logger.info("Testing completed successfully")
        
    except Exception as e:
        logger.exception(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    run_benchmark()