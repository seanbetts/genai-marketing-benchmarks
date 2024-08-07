import pandas as pd
import sqlite3
import os
import re
from typing import Tuple, List, Dict, Any, Optional

from src.logger import get_logger
from src.constants import DATABASE_PATH, VALID_ANSWERS

logger = get_logger()

def estimate_cost(num_questions: int, num_rounds: int, selected_models: List[Dict[str, Any]], avg_prompt_tokens: int = 70, avg_completion_tokens: int = 1) -> Tuple[float, List[Tuple[str, float]]]:
    """
    Estimate the cost of running the tests.
    
    Args:
    num_questions (int): Number of questions per round
    num_rounds (int): Number of rounds to run
    selected_models (List[Dict[str, Any]]): List of selected model dictionaries
    avg_prompt_tokens (int): Average number of tokens in a prompt
    avg_completion_tokens (int): Average number of tokens in a completion
    
    Returns:
    Tuple[float, List[Tuple[str, float]]]: (total_estimated_cost, list of (model_name, model_cost) tuples)
    """
    logger.info("Calculating estimated cost")

    total_questions = num_questions * num_rounds
    
    model_costs = [
        (model['name'], 
         total_questions * ((model['prompt'] * avg_prompt_tokens) + (model['completion'] * avg_completion_tokens)))
        for model in selected_models
    ]

    total_cost = sum(cost for _, cost in model_costs)

    for model_name, model_cost in model_costs:
        logger.info(f"Estimated cost for {model_name}: ${model_cost:.3f}")

    return total_cost, model_costs

def calculate_token_cost(prompt_tokens: int, completion_tokens: int, model_info: Dict[str, Any]) -> float:
    """
    Calculate the cost of tokens used.
    
    Args:
    prompt_tokens (int): Number of tokens in the prompt
    completion_tokens (int): Number of tokens in the completion
    model_info (Dict[str, Any]): Dictionary containing model information including pricing
    
    Returns:
    float: Total cost
    """
    prompt_cost = prompt_tokens * model_info["prompt"]
    completion_cost = completion_tokens * model_info["completion"]
    return prompt_cost + completion_cost

def load_questions(db_path: str = DATABASE_PATH, table_name: str = 'questions') -> pd.DataFrame:
    """
    Load questions from the SQLite database.
    
    Args:
    db_path (str): Path to the database
    table_name (str): Name of the table containing questions
    
    Returns:
    pd.DataFrame: Dataframe containing the questions
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at path: {db_path}")
    
    conn = sqlite3.connect(db_path)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def answer_check(answer: str) -> Tuple[str, bool]:
    """
    Check if the answer is valid.
    
    Args:
    answer (str): The answer to check
    
    Returns:
    Tuple[str, bool]: Cleaned answer and whether it's valid
    """
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

def check_table_exists_and_get_highest_round(model_variant: str, today_date: str, db_path: str = DATABASE_PATH) -> int:
    """
    Check if a table exists for the given model and date, and get the highest round number.
    
    Args:
    model_variant (str): The variant of the model being tested
    today_date (str): The current date in 'YYYY-MM-DD' format
    db_path (str): Path to the database
    
    Returns:
    int: The highest round number for the day, or 0 if the table doesn't exist
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    model_cleaned = model_variant.split('/')[-1]
    table_name = f"{today_date}_{model_cleaned}".replace('-', '_').replace(':', '_').replace(' ', '_').replace('.', '_')
    
    logger.info(f"Checking for existing table: {table_name}")
    
    cursor.execute(f'SELECT name FROM sqlite_master WHERE type="table" AND name="{table_name}";')
    table_exists = cursor.fetchone()
    
    highest_round = 0
    if table_exists:
        logger.info(f"Table {table_name} exists, retrieving highest round number")
        # Table exists, retrieve the highest round number
        cursor.execute(f'SELECT MAX("Round") FROM "{table_name}";')
        result = cursor.fetchone()
        highest_round = result[0] if result[0] is not None else 0
    else:
        logger.info(f"Table {table_name} does not exist")
    
    conn.close()
    
    logger.info(f"Highest round number for {model_variant} on {today_date}: {highest_round}")
    return highest_round

def sanitize_column_name(col_name: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_]', '_', col_name)

def save_results_to_sqlite(iteration_results_df: pd.DataFrame, model: str, today_date: str, db_path: str = DATABASE_PATH) -> None:
    """
    Save results to SQLite database.
    
    Args:
    iteration_results_df (pandas.DataFrame): Dataframe containing the results
    model (str): Name of the model used
    base_folder (str): Base folder path
    today_date (str): Current date
    db_path (str): Path to the database
    """
    logger.info(f"Saving results for model {model} to SQLite database")
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

def get_sqlite_type(dtype: Any) -> str:
    if dtype == 'int64':
        return 'INTEGER'
    elif dtype == 'float64':
        return 'REAL'
    else:
        return 'TEXT'

def ensure_summary_table(conn: sqlite3.Connection, table_name: str, columns: pd.Index) -> None:
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (Model TEXT, Round INTEGER, Date TEXT)")
    cursor.execute(f"PRAGMA table_info({table_name})")
    existing_columns = [info[1] if isinstance(info, tuple) else info['name'] for info in cursor.fetchall()]
    new_columns = [sanitize_column_name(col) for col in columns if sanitize_column_name(col) not in existing_columns]
    for safe_col in new_columns:
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {safe_col} REAL")