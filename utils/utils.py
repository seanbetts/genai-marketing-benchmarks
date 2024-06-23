# Generate Provider based on Model
import re
import os
import platform
import sqlite3

# Clear console
def clear_console():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def determine_provider(model_name):
    model_name_lower = model_name.lower()  # Convert to lower case for case insensitive comparison
    if 'claude' in model_name_lower:
        return 'Anthropic'
    elif 'gpt' in model_name_lower:
        return 'OpenAI'
    elif 'gemini' in model_name_lower:
        return 'Google'
    elif 'llama' in model_name_lower:
        return 'Meta'
    elif 'mistral' in model_name_lower:
        return 'Mistral'
    else:
        return 'Unknown'

# Clean up Model names for each provider
def clean_model_name(model_name, provider):
    if provider == 'Anthropic':
        # Remove date-like strings
        model_name = re.sub(r'\d{8}', '', model_name)
        # Replace hyphens with spaces
        model_name = model_name.replace('-', ' ')
        # Format numbers correctly
        model_name = re.sub(r'(\d) (\d)', r'\1.\2', model_name)
        # Capitalize and format with a space after the model number
        model_name_parts = model_name.split()
        model_name = f"{model_name_parts[0].title()}-{model_name_parts[1]} {model_name_parts[2].title()}"
    elif provider == 'OpenAI':
        # Remove date-like strings and trailing segments
        model_name = re.sub(r'\d{4}[-/]?\d{2}[-/]?\d{2}', '', model_name)
        model_name = re.sub(r'-\d+$', '', model_name)
        # Add hyphen after GPT, lowercase the "o", and remove trailing hyphens
        model_name = model_name.upper().replace(' ', '').replace('GPT', 'GPT-')
        model_name = re.sub(r'(\d)O', r'\1o', model_name)
        model_name = re.sub(r'-+', '-', model_name).rstrip('-')
        # Capitalize Turbo correctly and replace hyphen with space
        model_name = model_name.replace('TURBO', 'Turbo')
        model_name = model_name.replace('-Turbo', ' Turbo')
    elif provider == 'Google':
        # Remove date-like strings if any
        model_name = re.sub(r'\d{4}[-/]?\d{2}[-/]?\d{2}', '', model_name)
        # Add hyphen after Gemini
        model_name = model_name.replace('Gemini', 'Gemini-')
        # Capitalize first letter of each word and format correctly
        model_name = re.sub(r'(\b[a-z])', lambda x: x.group().upper(), model_name)
        # Remove last hyphen before type
        model_name = re.sub(r'-(Pro|Flash)$', r' \1', model_name)
    elif provider == 'Meta':
        # Remove everything before the forward slash
        model_name = model_name.split('/')[-1]
        # Remove date-like strings and trailing segments
        model_name = re.sub(r'\d{4}[-/]?\d{2}[-/]?\d{2}', '', model_name)
        # Add a hyphen after 'Llama'
        model_name = re.sub(r'(Llama) (\d)', r'\1-\2', model_name)
        # Remove everything after the 'B'
        model_name = re.sub(r'b.*', 'B', model_name)
        # Capitalize properly
        model_name = model_name.title()
        # Remove any extra hyphen or space after B
        model_name = re.sub(r'(\d)B', r'\1B', model_name)
        # Ensure there's no trailing hyphen or space
        model_name = model_name.strip('- ')
        model_name = model_name.replace('2-', '2 ')
        model_name = model_name.replace('3-', '3 ')
    elif provider == 'Mistral':
        # Remove everything before the forward slash
        model_name = model_name.split('/')[-1]
        # Remove "Instruct" and anything after
        model_name = re.sub(r'Instruct.*', '', model_name, flags=re.IGNORECASE)
        # Convert "X" to lowercase
        model_name = re.sub(r'X(\d)', r'x\1', model_name)
        # Remove trailing hyphen
        model_name = model_name.rstrip('-')
        # Capitalize properly
        model_name = re.sub(r'(\b[a-z])', lambda x: x.group().upper(), model_name)
    else:
        # Generic cleanup
        model_name = model_name.replace('-', ' ')
    return model_name

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

# Define a function to check the answers
def answer_check(logger, answer):
    valid_answers = ['A', 'B', 'C', 'D']
    answer = answer.upper().strip()
    if answer.startswith(('##', '**')):
        answer = answer[2:].strip()  # Remove '##' or '**' and strip any leading/trailing spaces
    elif answer.startswith(('#', '*')):
        answer = answer[1:].strip()  # Remove '#' or '*' and strip any leading/trailing spaces
    answer = answer[0] if answer else ''  # Keep only the first character if it exists
    if not answer or answer not in valid_answers:
        logger.warning(f"Invalid answer received: {answer}. Retrying...")
        return answer, False
    return answer, True

# Define a function to calculate the cost of tokens used
def calculate_token_cost(prompt_tokens, completion_tokens, model):
    prompt_cost = prompt_tokens * model["prompt"]
    completion_cost = completion_tokens * model["completion"]
    total_cost = prompt_cost + completion_cost
    return total_cost

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

# Function to save results to a CSV file in a new folder with today's date and current time
def save_results_to_csv(base_folder, today_date, logger, final_results_df, models, folder_name, current_time):
    folder_name = os.path.join(base_folder, today_date)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file_path = os.path.join(folder_name, f"{'_'.join([model['variant'] for model in models])}_{current_time}.csv")
    final_results_df.to_csv(file_path, index=False)
    logger.info(f"Results saved to {file_path}")

def save_results_to_sqlite(logger, iteration_results_df, model, base_folder, today_date, current_time):
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

    # Prepare the model summary data
    model_summary_data = {
        'Model': model,
        'Round': round_number,
        'Date': today_date,
        'Percentage_Correct': percentage_correct
    }

    # Save the model summary data to the model_summary table
    model_summary_df = pd.DataFrame([model_summary_data])
    model_summary_df.to_sql('model_summary', conn, if_exists='append', index=False)

    # Prepare the discipline summary data
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

    # Prepare the category summary data
    category_summary = iteration_results_df.groupby('Category')['Correct'].mean() * 100
    category_summary = category_summary.round(2)  # Round to two decimal places
    category_summary_data = {
        'Model': model,
        'Round': round_number,
        'Date': today_date,
        'TOTAL': percentage_correct,
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