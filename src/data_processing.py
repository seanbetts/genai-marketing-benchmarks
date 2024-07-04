import pandas as pd
import sqlite3
import os
from datetime import datetime
import re
from src.logger import get_logger
from src.constants import DATABASE_PATH, VALID_ANSWERS

logger = get_logger()

def estimate_cost(num_questions, num_rounds, selected_models, avg_prompt_tokens=70, avg_completion_tokens=1):
    """
    Estimate the cost of running the tests.
    
    Args:
    num_questions (int or str): Number of questions per round ('all' or int)
    num_rounds (int): Number of rounds to run
    selected_models (list): List of selected model dictionaries
    avg_prompt_tokens (int): Average number of tokens in a prompt
    avg_completion_tokens (int): Average number of tokens in a completion
    
    Returns:
    tuple: (total_estimated_cost, list of (model_name, model_cost) tuples)
    """
    logger.info("Calculating estimated cost")
    total_cost = 0
    model_costs = []

    for model in selected_models:
        model_name = model['name']
        prompt_cost = model['prompt']
        completion_cost = model['completion']

        # Calculate costs
        total_prompt_tokens = num_questions * num_rounds * avg_prompt_tokens
        total_completion_tokens = num_questions * num_rounds * avg_completion_tokens
        
        prompt_cost_total = total_prompt_tokens * prompt_cost
        completion_cost_total = total_completion_tokens * completion_cost
        
        model_total_cost = prompt_cost_total + completion_cost_total
        
        model_costs.append((model_name, model_total_cost))
        total_cost += model_total_cost

        logger.info(f"Estimated cost for {model_name}: ${model_total_cost:.3f}")

    logger.info(f"Total estimated cost: ${total_cost:.3f}")
    return total_cost, model_costs

def calculate_token_cost(prompt_tokens, completion_tokens, model_info):
    """
    Calculate the cost of tokens used.
    
    Args:
    prompt_tokens (int): Number of tokens in the prompt
    completion_tokens (int): Number of tokens in the completion
    model_info (dict): Dictionary containing model information including pricing
    
    Returns:
    float: Total cost
    """
    prompt_cost = prompt_tokens * model_info["prompt"]
    completion_cost = completion_tokens * model_info["completion"]
    return prompt_cost + completion_cost

def load_questions(table_name='questions'):
    """Load questions from the SQLite database."""
    if not os.path.exists(DATABASE_PATH):
        raise FileNotFoundError(f"Database file not found at path: {DATABASE_PATH}")
    
    conn = sqlite3.connect(DATABASE_PATH)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def answer_check(answer):
    """Check if the answer is valid."""
    logger.info(f"Checking answer: {answer}")
    answer = answer.upper().strip()
    if answer.startswith(('##', '**')):
        answer = answer[2:].strip()
    elif answer.startswith(('#', '*')):
        answer = answer[1:].strip()
    answer = answer[0] if answer else ''
    
    is_valid = answer in VALID_ANSWERS
    if not is_valid:
        logger.warning(f"Invalid answer received: {answer}")
    else:
        logger.info(f"Valid answer: {answer}")
    
    return answer, is_valid

def sanitize_column_name(col_name):
    return re.sub(r'[^a-zA-Z0-9_]', '_', col_name)

def save_results_to_sqlite(iteration_results_df, model, base_folder, today_date, current_time):
    """
    Save results to SQLite database.
    
    Args:
    iteration_results_df (pandas.DataFrame): Dataframe containing the results
    model (str): Name of the model used
    base_folder (str): Base folder path
    today_date (str): Current date
    current_time (str): Current time
    """
    logger.info(f"Saving results for model {model} to SQLite database")
    db_path = os.path.join(base_folder, 'results_database.sqlite')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    model_cleaned = model.split('/')[-1]
    table_name = f"{today_date}_{model_cleaned}".replace('-', '_').replace(':', '_').replace(' ', '_').replace('.', '_')
    quoted_table_name = f'"{table_name}"'
    
    # Check if table exists
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    table_exists = cursor.fetchone() is not None
    
    if not table_exists:
        # Create table with columns from the DataFrame
        columns = [f"{sanitize_column_name(col)} {get_sqlite_type(iteration_results_df[col].dtype)}" for col in iteration_results_df.columns]
        create_table_sql = f"CREATE TABLE {quoted_table_name} ({', '.join(columns)})"
        cursor.execute(create_table_sql)
    else:
        # Check existing columns and add any missing ones
        cursor.execute(f"PRAGMA table_info({quoted_table_name})")
        existing_columns = [info[1] for info in cursor.fetchall()]
        
        for column in iteration_results_df.columns:
            if column not in existing_columns:
                safe_column_name = sanitize_column_name(column)
                column_type = get_sqlite_type(iteration_results_df[column].dtype)
                cursor.execute(f"ALTER TABLE {quoted_table_name} ADD COLUMN {safe_column_name} {column_type}")
    
    # Save the results
    iteration_results_df.to_sql(table_name, conn, if_exists='append', index=False)
    
    # Calculate and save summary data
    round_number = int(iteration_results_df['Round'].iloc[0])
    total_questions = len(iteration_results_df)
    correct_answers = iteration_results_df['Is_Correct'].sum()
    percentage_correct = round((correct_answers / total_questions) * 100, 2)
    
    # Model summary
    model_summary_data = {
        'Model': [model],
        'Round': [round_number],
        'Date': [today_date],
        'Percentage_Correct': [percentage_correct]
    }
    model_summary_df = pd.DataFrame(model_summary_data)
    model_summary_df.to_sql('model_summary', conn, if_exists='append', index=False)
    
    # Discipline summary
    if 'Discipline' in iteration_results_df.columns:
        discipline_summary = iteration_results_df.groupby('Discipline')['Is_Correct'].mean() * 100
        discipline_summary = discipline_summary.round(2)
        discipline_summary_data = {
            'Model': model,
            'Round': round_number,
            'Date': today_date,
        }
        discipline_summary_data.update(discipline_summary.to_dict())
        
        ensure_summary_table(conn, 'discipline_summary', discipline_summary.index)
        
        discipline_summary_df = pd.DataFrame([discipline_summary_data])
        discipline_summary_df.to_sql('discipline_summary', conn, if_exists='append', index=False)
    
    # Category summary
    if 'Category' in iteration_results_df.columns:
        category_summary = iteration_results_df.groupby('Category')['Is_Correct'].mean() * 100
        category_summary = category_summary.round(2)
        category_summary_data = {
            'Model': model,
            'Round': round_number,
            'Date': today_date,
            'TOTAL': percentage_correct,
        }
        category_summary_data.update({sanitize_column_name(cat): val for cat, val in category_summary.to_dict().items()})
        
        ensure_summary_table(conn, 'category_summary', category_summary.index)
        
        category_summary_df = pd.DataFrame([category_summary_data])
        category_summary_df.to_sql('category_summary', conn, if_exists='append', index=False)
    
    conn.close()

    logger.info(f"Results saved to database successfully in table {table_name}. Overall percentage correct: {percentage_correct}%")

def get_sqlite_type(dtype):
    if dtype == 'int64':
        return 'INTEGER'
    elif dtype == 'float64':
        return 'REAL'
    else:
        return 'TEXT'

def ensure_summary_table(conn, table_name, columns):
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (Model TEXT, Round INTEGER, Date TEXT)")
    cursor.execute(f"PRAGMA table_info({table_name})")
    existing_columns = [info[1] for info in cursor.fetchall()]
    for col in columns:
        safe_col = sanitize_column_name(col)
        if safe_col not in existing_columns:
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {safe_col} REAL")