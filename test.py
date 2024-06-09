import pandas as pd
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
import sqlite3
from openai import OpenAI
import anthropic
import google.generativeai as gemini
from together import Together
import curses
import platform
import re
import time
import threading

# Clear console
if platform.system() == "Windows":
    os.system('cls')
else:
    os.system('clear')

# Load environment variables
load_dotenv()

# Get current date and time
today_date = datetime.today().strftime('%Y-%m-%d')
current_time = datetime.now().strftime('%H-%M')

# Set up folder
base_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logs_folder = os.path.join(base_folder, 'Logs')
today_logs_folder = os.path.join(logs_folder, today_date)
if not os.path.exists(today_logs_folder):
    os.makedirs(today_logs_folder)

# Load the questions table into a pandas DataFrame
db_path = os.path.join(base_folder, 'results_database.sqlite')
table_name = 'questions'
if not os.path.exists(db_path):
    raise FileNotFoundError(f"Database file not found at path: {db_path}")
conn = sqlite3.connect(db_path)
query = f"SELECT * FROM {table_name}"
df = pd.read_sql_query(query, conn)
conn.close()

# Set up your OpenAI API key
GPT_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Set up your Claude API key
claude_client = anthropic.Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))

# Set up your Gemini API key
gemini_client = gemini.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Set up Together API key
together_client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

# Define LLMs
llms = [
    {"name": "GPT-3.5 Turbo", "variant": "gpt-3.5-turbo-0125", "provider": "OpenAI", "prompt": 0.50 / 1000000, "completion": 1.50 / 1000000},
    {"name": "GPT-4", "variant": "gpt-4-0613", "provider": "OpenAI", "prompt": 30 / 1000000, "completion": 60 / 1000000},
    {"name": "GPT-4 Turbo", "variant": "gpt-4-turbo-2024-04-09", "provider": "OpenAI", "prompt": 10 / 1000000, "completion": 30 / 1000000},
    {"name": "GPT-4o", "variant": "gpt-4o-2024-05-13", "provider": "OpenAI", "prompt": 5 / 1000000, "completion": 15 / 1000000},
    {"name": "Claude-3 Haiku", "variant": "claude-3-haiku-20240307", "provider": "Anthropic", "prompt": 0.25 / 1000000, "completion": 1.25 / 1000000},
    {"name": "Claude-3 Sonnet", "variant": "claude-3-sonnet-20240229", "provider": "Anthropic", "prompt": 3 / 1000000, "completion": 15 / 1000000},
    {"name": "Claude-3 Opus", "variant": "claude-3-opus-20240229", "provider": "Anthropic", "prompt": 15 / 1000000, "completion": 75 / 1000000},
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

def curses_menu(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    selected_rows = set()
    current_row = 0

    # Initialize color pair
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Select models (press Space to toggle, Enter to confirm):")
        for idx, model in enumerate(llms):
            x = 0
            y = idx + 1
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, f"{'[X]' if idx in selected_rows else '[ ]'} {model['name']} (Provider: {model['provider']})")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, f"{'[X]' if idx in selected_rows else '[ ]'} {model['name']} (Provider: {model['provider']})")
        
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(llms) - 1:
            current_row += 1
        elif key == ord(' '):  # Handle Space key
            if current_row in selected_rows:
                selected_rows.remove(current_row)
            else:
                selected_rows.add(current_row)
        elif key in [10, 13]:  # Handle Enter key
            break
        
        stdscr.refresh()

    selected_models = [llms[idx] for idx in selected_rows]
    return selected_models

# Use curses.wrapper to call the curses_menu function once
selected_models = curses.wrapper(curses_menu)

# Create log file
log_file = os.path.join(today_logs_folder, f"{'_'.join([model['variant'].replace('/', '_') for model in selected_models])}_{current_time}.log")

# Create and configure logger
logger = logging.getLogger(__name__)
for handler in logger.handlers[:]:  # Iterate and remove all handlers if any are set by default
    logger.removeHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False

# Create handlers
file_handler = logging.FileHandler(log_file)
console_handler = logging.StreamHandler()

# Create formatters and add it to handlers
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Validate the choices
if not selected_models:
    raise ValueError("No models selected. Please run the script again and choose at least one model.")

def curses_category_menu(stdscr, categories):
    curses.curs_set(0)
    stdscr.clear()
    selected_rows = set(range(len(categories)))
    current_row = 0

    # Initialize color pair
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Select categories (press Space to toggle, Enter to confirm):")
        for idx, category in enumerate(categories):
            x = 0
            y = idx + 1
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, f"{'[X]' if idx in selected_rows else '[ ]'} {category}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, f"{'[X]' if idx in selected_rows else '[ ]'} {category}")
        
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(categories) - 1:
            current_row += 1
        elif key == ord(' '):  # Handle Space key
            if current_row in selected_rows:
                selected_rows.remove(current_row)
            else:
                selected_rows.add(current_row)
        elif key in [10, 13]:  # Handle Enter key
            break
        
        stdscr.refresh()

    selected_categories = [categories[idx] for idx in selected_rows]
    return selected_categories

# Use curses.wrapper to call the curses_category_menu function once
selected_categories = curses.wrapper(curses_category_menu, df['Category'].unique().tolist())

# Filter the DataFrame based on the selected categories
filtered_df = df[df['Category'].isin(selected_categories)]

# Prompt the user to enter the number of questions and rounds
num_questions_input = input("Enter the number of questions to test (or type 'All' to use all questions): ")
num_questions = len(filtered_df) if num_questions_input.lower() == 'all' else int(num_questions_input)
num_rounds = int(input("Enter the number of rounds to run: "))
retry_count = 3

# Function to estimate the cost of the test run
def estimate_cost(num_questions, num_rounds, avg_prompt_tokens, avg_completion_tokens, selected_models):
    total_cost = 0
    model_costs = []
    for model in selected_models:
        total_prompt_tokens = num_questions * num_rounds * avg_prompt_tokens
        total_completion_tokens = num_questions * num_rounds * avg_completion_tokens
        total_prompt_cost = total_prompt_tokens * model["prompt"]
        total_completion_cost = total_completion_tokens * model["completion"]
        model_total_cost = total_prompt_cost + total_completion_cost
        model_costs.append((model["name"], model_total_cost))
        total_cost += model_total_cost
    return total_cost, model_costs

# Estimate the cost
avg_prompt_tokens = 70
avg_completion_tokens = 1
estimated_cost, model_costs = estimate_cost(num_questions, num_rounds, avg_prompt_tokens, avg_completion_tokens, selected_models)

# Print estimated costs for each model
print(f"\nEstimated cost for running {num_rounds} rounds with {num_questions} questions each across selected models:")
for model_name, cost in model_costs:
    print(f"  {model_name}: ${cost:.3f}")
print(f"Total estimated cost: ${estimated_cost:.3f}")

# Ask for user confirmation to proceed
confirm = input("\nDo you want to proceed with the testing run? (y/n): ").strip().lower()
if confirm != 'y':
    print("Testing run aborted by the user.")
    exit()
logger.info(f"Estimated cost for running {num_rounds} rounds with {num_questions} questions each across selected models: ${estimated_cost:.3f}")

# Define a function to call LLM API
def ask_llm(provider, model, question, choices, retry_count):
    def make_prompt(question, choices):
        return f"Choose the correct answer for the following multiple-choice question. ANSWER ONLY with a SINGLE letter of the correct choice.\n\nQuestion: {question}\n\nChoices:\n{choices}\n\nAnswer:"

    def handle_response(response, provider):
        if provider == 'OpenAI':
            return response.choices[0].message.content.strip()
        elif provider == 'Anthropic':
            return response.content[0].text
        elif provider == 'Google':
            return response.text
        elif provider in ['Meta', 'Mistral']:
            return response.choices[0].message.content

    def handle_tokens(response, provider, prompt=None, answer=None, model_instance=None):
        if provider == 'OpenAI':
            return response.usage.prompt_tokens, response.usage.completion_tokens
        elif provider == 'Anthropic':
            return response.usage.input_tokens, response.usage.output_tokens
        elif provider == 'Google':
            return model_instance.count_tokens(prompt).total_tokens, model_instance.count_tokens(answer).total_tokens
        elif provider in ['Meta', 'Mistral']:
            return response.usage.prompt_tokens, response.usage.completion_tokens
        else:
            return 0, 0
        
    # Create a decorator to enforce rate limit
    def rate_limited(max_per_second):
        min_interval = 1.0 / max_per_second
        lock = threading.Lock()
        last_time_called = [0.0]

        def decorator(func):
            def wrapped(*args, **kwargs):
                with lock:
                    elapsed = time.time() - last_time_called[0]
                    left_to_wait = min_interval - elapsed
                    if left_to_wait > 0:
                        time.sleep(left_to_wait)
                    last_time_called[0] = time.time()
                    return func(*args, **kwargs)
            return wrapped
        return decorator
    
    @rate_limited(1 / 1.1)  # Allow only one call per 1.1 seconds
    def rate_limited_api_call(model, prompt):
        return together_client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}]), None

    def make_api_call(provider, model, prompt):
        try:
            if provider == 'OpenAI':
                return GPT_client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}]), None
            elif provider == 'Anthropic':
                return claude_client.messages.create(model=model, max_tokens=1024, messages=[{"role": "user", "content": prompt}]), None
            elif provider == 'Google':
                model_instance = gemini.GenerativeModel(model)
                return model_instance.generate_content(prompt), model_instance
            elif provider in ['Meta', 'Mistral']:
                return rate_limited_api_call(model, prompt)

        except Exception as e:
            logger.error(f"Error during API call: {e}")
            return None, None

    if retry_count == 0:
        logger.warning("Maximum retries reached, returning None.")
        return None, 0, 0

    prompt = make_prompt(question, choices)
    response, model_instance = make_api_call(provider, model, prompt)

    if not response:
        return ask_llm(provider, model, question, choices, retry_count - 1)

    answer = handle_response(response, provider)
    answer, valid = answer_check(question, answer)

    if not valid:
        return ask_llm(provider, model, question, choices, retry_count - 1)

    prompt_tokens, completion_tokens = handle_tokens(response, provider, prompt, answer, model_instance)
    return answer, prompt_tokens, completion_tokens

# Define a function to check the answers
def answer_check(question, answer):
    valid_answers = ['A', 'B', 'C', 'D']
    answer = answer.upper().strip()
    if not answer or answer[0] not in valid_answers:
        logger.warning(f"Invalid answer received: {answer}. Retrying...")
        return answer, False
    return answer[0], True

# Define a function to calculate the cost of tokens used
def calculate_token_cost(prompt_tokens, completion_tokens, model):
    prompt_cost = prompt_tokens * model["prompt"]
    completion_cost = completion_tokens * model["completion"]
    total_cost = prompt_cost + completion_cost
    return total_cost

# Function to test a specified number of questions
def test_llm_with_questions(df, num_questions, num_rounds, initial_rounds, selected_models):
    def get_column_value(row, primary_col, fallback_col):
        return row.get(primary_col, row.get(fallback_col, None))
    all_results = []
    try:
        for model_info in selected_models:
            initial_round = initial_rounds[model_info['variant']]
            for iteration in range(initial_round, initial_round + num_rounds):
                results = []
                model_name = model_info["name"]
                model_variant = model_info["variant"]
                provider = model_info["provider"]
                logger.info(f"Starting Round {iteration + 1} for {model_name}")
                for index, row in df.head(num_questions).iterrows():
                    discipline = row['Discipline']
                    category = row['Category']
                    sub_category = get_column_value(row, 'Sub-Category', 'Sub_Category')
                    question = row['Question']
                    difficulty = row['Difficulty']
                    option_a = get_column_value(row, 'Option A', 'Option_A')
                    option_b = get_column_value(row, 'Option B', 'Option_B')
                    option_c = get_column_value(row, 'Option C', 'Option_C')
                    option_d = get_column_value(row, 'Option D', 'Option_D')
                    choices = f"""A. {option_a}\nB. {option_b}\nC. {option_c}\nD. {option_d}"""
                    correct_answer = get_column_value(row, 'Correct Option', 'Correct_Option')
                    logger.info(f"Round {iteration + 1}: Asked question #{index + 1}: {question}")
                    llm_answer, prompt_tokens, completion_tokens = ask_llm(provider, model_variant, question, choices, retry_count)
                    is_correct = llm_answer == correct_answer
                    logger.info(f"Round {iteration + 1}: {model_name} Answer #{index + 1}: {llm_answer}, {is_correct}")
                    cost = calculate_token_cost(prompt_tokens, completion_tokens, model_info)
                    timestamp = datetime.now()
                    results.append({
                        'Round': iteration + 1,
                        'Discipline': discipline,
                        'Category': category,
                        'Sub_Category': sub_category,
                        'Question': question,
                        'Difficulty': difficulty,
                        'Correct_Answer': correct_answer,
                        'Provider': provider,
                        'Model': model_name,
                        'Answer': llm_answer,
                        'Correct': is_correct,
                        'Cost': cost,
                        'Timestamp': timestamp
                    })

                # Combine results of each iteration
                iteration_results_df = pd.DataFrame(results)
                all_results.append(iteration_results_df)

                # Save the iteration results
                save_results_to_sqlite(iteration_results_df, model_variant, base_folder, today_date, current_time)
                logger.info(f"Finished Round {iteration + 1} for {model_name}")

    except KeyboardInterrupt:
        logger.info("Script interrupted by user.")
        # Perform any necessary cleanup here
        pass

    # Combine all iterations into one DataFrame
    if all_results:  # Check if there are any results to concatenate
        final_results_df = pd.concat(all_results, ignore_index=True)
    else:
        final_results_df = pd.DataFrame()  # Return an empty DataFrame if no results

    return final_results_df


# Function to save results to a CSV file in a new folder with today's date and current time
def save_results_to_csv(final_results_df, models, folder_name, current_time):
    folder_name = os.path.join(base_folder, today_date)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file_path = os.path.join(folder_name, f"{'_'.join([model['variant'] for model in models])}_{current_time}.csv")
    final_results_df.to_csv(file_path, index=False)
    logger.info(f"Results saved to {file_path}")

# Function to check if rounds have already been run today
def check_table_exists_and_get_highest_round(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f'SELECT name FROM sqlite_master WHERE type="table" AND name="{table_name}";')
    table_exists = cursor.fetchone()
    
    highest_round = 0
    if table_exists:
        # Table exists, retrieve the highest round number
        cursor.execute(f'SELECT MAX("Round") FROM "{table_name}";')
        highest_round = cursor.fetchone()[0]
        if highest_round is None:
            highest_round = 0

    return highest_round

def save_results_to_sqlite(iteration_results_df, model, base_folder, today_date, current_time):
    def sanitize_column_name(col_name):
        return re.sub(r'[^a-zA-Z0-9_]', '_', col_name)

    # Define the database file path (use a general name for the database)
    db_path = os.path.join(base_folder, 'results_database.sqlite')

    # Create a connection to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Generate a unique table name based on the model and current date
    model_cleaned = model.split('/')[-1]
    table_name = f"{today_date}_{model_cleaned}".replace('-', '_').replace(':', '_').replace(' ', '_').replace('.', '_')

    # Sanitize DataFrame column names
    iteration_results_df.columns = [sanitize_column_name(col) for col in iteration_results_df.columns]

    # Save the DataFrame to the SQLite table
    iteration_results_df.to_sql(table_name, conn, if_exists='append', index=False)

    # Calculate the summary data
    round_number = int(iteration_results_df['Round'].iloc[0])  # Ensure the round number is an integer
    total_questions = len(iteration_results_df)
    correct_answers = iteration_results_df['Correct'].sum()
    percentage_correct = round((correct_answers / total_questions) * 100, 2)  # Round to two decimal places

    # Prepare the summary data
    model_summary_data = {
        'Model': model,
        'Round': round_number,
        'Date': today_date,
        'Percentage_Correct': percentage_correct
    }

    # Save the model summary data to the model_summary table
    model_summary_df = pd.DataFrame([model_summary_data])
    model_summary_df.to_sql('model_summary', conn, if_exists='append', index=False)

    # Calculate the discipline summary data
    discipline_summary = iteration_results_df.groupby('Discipline')['Correct'].mean() * 100
    discipline_summary = discipline_summary.round(2)  # Round to two decimal places
    discipline_summary_data = {
        'Model': model,
        'Round': round_number,
        'Date': today_date,
    }
    discipline_summary_data.update(discipline_summary.to_dict())

    # Prepare the discipline summary DataFrame
    discipline_summary_df = pd.DataFrame([discipline_summary_data])

    # Ensure the discipline summary table has the correct columns
    cursor.execute("CREATE TABLE IF NOT EXISTS discipline_summary (Model TEXT, Round INTEGER, Date TEXT)")
    cursor.execute("PRAGMA table_info(discipline_summary)")
    existing_columns = [info[1] for info in cursor.fetchall()]
    for col in discipline_summary.index:
        safe_col = sanitize_column_name(col)
        if safe_col not in existing_columns:
            cursor.execute(f"ALTER TABLE discipline_summary ADD COLUMN {safe_col} REAL")

    # Ensure the Round column in discipline_summary_df is an integer
    discipline_summary_df['Round'] = discipline_summary_df['Round'].astype(int)

    # Save the discipline summary data to the discipline_summary table
    discipline_summary_df.to_sql('discipline_summary', conn, if_exists='append', index=False)

    # Calculate the category summary data
    category_summary = iteration_results_df.groupby('Category')['Correct'].mean() * 100
    category_summary = category_summary.round(2)  # Round to two decimal places
    category_summary_data = {
        'Model': model,
        'Round': round_number,
        'Date': today_date,
    }
    category_summary_data.update({sanitize_column_name(cat): val for cat, val in category_summary.to_dict().items()})

    # Prepare the category summary DataFrame
    category_summary_df = pd.DataFrame([category_summary_data])

    # Ensure the category summary table has the correct columns
    cursor.execute("CREATE TABLE IF NOT EXISTS category_summary (Model TEXT, Round INTEGER, Date TEXT)")
    cursor.execute("PRAGMA table_info(category_summary)")
    existing_columns = [info[1] for info in cursor.fetchall()]
    for col in category_summary.index:
        safe_col = sanitize_column_name(col)
        if safe_col not in existing_columns:
            cursor.execute(f"ALTER TABLE category_summary ADD COLUMN {safe_col} REAL")

    # Ensure the Round column in category_summary_df is an integer
    category_summary_df['Round'] = category_summary_df['Round'].astype(int)

    # Save the category summary data to the category_summary table
    category_summary_df.to_sql('category_summary', conn, if_exists='append', index=False)

    # Close the database connection
    conn.close()

    logger.info(f"Results saved to SQLite database results_database.sqlite in table {table_name}")

# Check for existing table and get initial round number for each model
initial_rounds = {}
conn = sqlite3.connect(os.path.join(base_folder, 'results_database.sqlite'))
for model in selected_models:
    table_name = f"{today_date}_{model['variant']}".replace('-', '_').replace(':', '_').replace(' ', '_').replace('.', '_')
    model_initial_round = check_table_exists_and_get_highest_round(conn, table_name)
    initial_rounds[model['variant']] = model_initial_round
conn.close()

# Update the test_llm_with_questions function call to use initial_rounds
final_results_df = test_llm_with_questions(filtered_df, num_questions, num_rounds, initial_rounds, selected_models)

# Display the results
if final_results_df.empty:
    print("No results to display. The script was interrupted before any data could be processed.")
else:
    print(final_results_df)