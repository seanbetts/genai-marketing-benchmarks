import pandas as pd
import sqlite3
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

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

def load_questions(db_path, table_name='questions'):
    """
    Load questions from the SQLite database.
    
    Args:
    db_path (str): Path to the SQLite database
    table_name (str): Name of the table containing questions
    
    Returns:
    pandas.DataFrame: Dataframe containing the questions
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at path: {db_path}")
    
    conn = sqlite3.connect(db_path)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def answer_check(answer):
    """
    Check if the answer is valid.
    
    Args:
    answer (str): The answer to check
    
    Returns:
    tuple: (cleaned_answer, is_valid)
    """
    logger.info(f"Checking answer: {answer}")
    valid_answers = ['A', 'B', 'C', 'D']
    answer = answer.upper().strip()
    if answer.startswith(('##', '**')):
        answer = answer[2:].strip()  # Remove '##' or '**' and strip any leading/trailing spaces
    elif answer.startswith(('#', '*')):
        answer = answer[1:].strip()  # Remove '#' or '*' and strip any leading/trailing spaces
    answer = answer[0] if answer else ''  # Keep only the first character if it exists
    
    is_valid = answer in valid_answers
    if not is_valid:
        logger.warning(f"Invalid answer received: {answer}")
    else:
        logger.info(f"Valid answer: {answer}")
    
    return answer, is_valid

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
    db_path = os.path.join(base_folder, 'results_database.sqlite')
    conn = sqlite3.connect(db_path)
    
    model_cleaned = model.split('/')[-1]
    table_name = f"{today_date}_{model_cleaned}".replace('-', '_').replace(':', '_').replace(' ', '_').replace('.', '_')
    
    iteration_results_df.to_sql(table_name, conn, if_exists='append', index=False)
    
    # Calculate and save summary data
    round_number = int(iteration_results_df['Round'].iloc[0])
    total_questions = len(iteration_results_df)
    correct_answers = iteration_results_df['Is_Correct'].sum()
    percentage_correct = round((correct_answers / total_questions) * 100, 2)
    
    summary_data = {
        'Model': [model],
        'Round': [round_number],
        'Date': [today_date],
        'Percentage_Correct': [percentage_correct]
    }
    summary_df = pd.DataFrame(summary_data)
    summary_df.to_sql('model_summary', conn, if_exists='append', index=False)
    
    conn.close()

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