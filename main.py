import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from datetime import datetime

from src.api_calls import query_language_model
from src.data_processing import load_questions, save_results_to_sqlite, calculate_token_cost, estimate_cost
from src.user_interface import select_models, select_categories, get_user_inputs, confirm_run
from src.logger import setup_logger


# Define LLMs
llms = [
    {"name": "GPT-3.5 Turbo", "variant": "gpt-3.5-turbo-0125", "provider": "OpenAI", "prompt": 0.50 / 1000000, "completion": 1.50 / 1000000},
    {"name": "GPT-4", "variant": "gpt-4-0613", "provider": "OpenAI", "prompt": 30 / 1000000, "completion": 60 / 1000000},
    {"name": "GPT-4 Turbo", "variant": "gpt-4-turbo-2024-04-09", "provider": "OpenAI", "prompt": 10 / 1000000, "completion": 30 / 1000000},
    {"name": "GPT-4o", "variant": "gpt-4o-2024-05-13", "provider": "OpenAI", "prompt": 5 / 1000000, "completion": 15 / 1000000},
    {"name": "Claude-3.5 Sonnet", "variant": "claude-3-5-sonnet-20240620", "provider": "Anthropic", "prompt": 3 / 1000000, "completion": 15 / 1000000},
    {"name": "Claude-3 Opus", "variant": "claude-3-opus-20240229", "provider": "Anthropic", "prompt": 15 / 1000000, "completion": 75 / 1000000},
    {"name": "Claude-3 Sonnet", "variant": "claude-3-sonnet-20240229", "provider": "Anthropic", "prompt": 3 / 1000000, "completion": 15 / 1000000},
    {"name": "Claude-3 Haiku", "variant": "claude-3-haiku-20240307", "provider": "Anthropic", "prompt": 0.25 / 1000000, "completion": 1.25 / 1000000},
    {"name": "Gemini-1.0 Pro", "variant": "gemini-1.0-pro", "provider": "Google", "prompt": 0.5 / 1000000, "completion": 1.5 / 1000000},
    {"name": "Gemini-1.5 Flash", "variant": "gemini-1.5-flash", "provider": "Google", "prompt": 0.35 / 1000000, "completion": 1.05 / 1000000},
    {"name": "Gemini-1.5 Pro", "variant": "gemini-1.5-pro", "provider": "Google", "prompt": 1.75 / 1000000, "completion": 10.5 / 1000000},
    {"name": "Llama-2-7B", "variant": "meta-llama/Llama-2-7b-chat-hf", "provider": "Meta", "prompt": 0.2/1000000, "completion": 0.2/1000000},
    {"name": "Llama-2-13B", "variant": "meta-llama/Llama-2-13b-chat-hf", "provider": "Meta", "prompt": 0.22/1000000, "completion": 0.22/1000000},
    {"name": "Llama-2-70B", "variant": "meta-llama/Llama-2-70b-chat-hf", "provider": "Meta", "prompt": 0.9/1000000, "completion": 0.9/1000000},
    {"name": "Llama-3-8B", "variant": "meta-llama/Llama-3-8b-chat-hf", "provider": "Meta", "prompt": 0.2/1000000, "completion": 0.2/1000000},
    {"name": "Llama-3-70B", "variant": "meta-llama/Llama-3-70b-chat-hf", "provider": "Meta", "prompt": 0.9/1000000, "completion": 0.9/1000000},
    {"name": "Mistral-7B", "variant": "mistralai/Mistral-7B-Instruct-v0.3", "provider": "Mistral", "prompt": 0.2/1000000, "completion": 0.2/1000000},
    {"name": "Mixtral-8x7B", "variant": "mistralai/Mixtral-8x7B-Instruct-v0.1", "provider": "Mistral", "prompt": 0.6/1000000, "completion": 0.6/1000000},
    {"name": "Mixtral-8x22B", "variant": "mistralai/Mixtral-8x22B-Instruct-v0.1", "provider": "Mistral", "prompt": 1.2/1000000, "completion": 1.2/1000000}
]

def main():
    # Set up logger
    base_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    logger = setup_logger(base_folder)

    logger.info("Starting the GenAI Marketing Benchmarks script")

    # Get current date and time
    today_date = datetime.today().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H-%M')

    # Select models
    logger.info("Prompting user to select models")
    selected_models = select_models(llms)
    logger.info(f"Selected models: {[model['name'] for model in selected_models]}")

    # Load questions
    logger.info("Loading questions from database")
    db_path = os.path.join(base_folder, 'results_database.sqlite')
    questions_df = load_questions(db_path)
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
    total_questions = len(filtered_df)

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
        for iteration in range(num_rounds):
            logger.info(f"Starting round {iteration + 1} for {model_info['name']}")
            results = []
            questions_to_test = filtered_df if num_questions == 'all' else filtered_df.sample(n=min(num_questions, total_questions))
            for index, question in questions_to_test.iterrows():
                logger.info(f"Processing question {index + 1}")
                # Prepare the prompt
                prompt = f"Choose the correct answer for the following marketing multiple-choice question. ANSWER ONLY with a SINGLE letter of the correct choice. DO NOT give an explanation.\n\nQuestion: {question['Question']}\nChoices:\nA. {question['Option_A']}\nB. {question['Option_B']}\nC. {question['Option_C']}\nD. {question['Option_D']}\nAnswer:"
                
                # Query the model
                logger.info(f"Querying model {model_info['name']}")
                answer, prompt_tokens, completion_tokens = query_language_model(
                    model_info['provider'],
                    model_info['variant'],
                    prompt
                )

                # Process the result
                is_correct = answer == question['Correct_Option']
                cost = calculate_token_cost(prompt_tokens, completion_tokens, model_info)

                logger.info(f"Answer: {answer}")
                logger.info(f"Question {index + 1} result: {is_correct}")

                # Store the result
                results.append({
                    'Round': iteration + 1,
                    'Question': question['Question'],
                    'Correct_Answer': question['Correct_Option'],
                    'Model_Answer': answer,
                    'Is_Correct': is_correct,
                    'Cost': cost
                })

            # Save results
            logger.info(f"Saving results for round {iteration + 1}")
            results_df = pd.DataFrame(results)
            save_results_to_sqlite(results_df, model_info['variant'], base_folder, today_date, current_time)

        logger.info(f"Completed all rounds for model: {model_info['name']}")

    logger.info("Testing completed successfully")
    print("Testing completed successfully.")

if __name__ == "__main__":
    main()