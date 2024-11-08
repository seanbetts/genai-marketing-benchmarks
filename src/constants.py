import os
import yaml
from typing import Dict, Any

# File paths
SCRIPTS_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_FOLDER = os.path.dirname(SCRIPTS_FOLDER)
LOGS_FOLDER = os.path.join(BASE_FOLDER, 'Logs')
CONFIG_PATH = os.path.join(SCRIPTS_FOLDER, 'config.yaml')

# Load configuration
def load_config(config_path: str = CONFIG_PATH) -> Dict[str, Any]:
    with open(config_path, 'r') as config_file:
        return yaml.safe_load(config_file)

CONFIG: Dict[str, Any] = load_config()

# Function to evaluate cost expressions
def evaluate_cost(expression: str) -> float:
    try:
        return eval(expression)
    except Exception as e:
        print(f"Error evaluating cost expression {expression}: {e}")
        return 0.0

# Database settings
DATABASE_NAME = CONFIG['database']['name']
DATABASE_FOLDER = CONFIG['database']['folder']
DATABASE_PATH = os.path.join(BASE_FOLDER, DATABASE_FOLDER, DATABASE_NAME)

# Vertex API settings
PROJECT_ID = CONFIG['api']['project_id']
LOCATION = CONFIG['api']['location']
SERVICE_ACCOUNT_FILE = os.path.join(SCRIPTS_FOLDER, 'key.json')

# Model definitions with calculated costs
MODELS = []
for model in CONFIG['models']:
    model['prompt'] = evaluate_cost(model['prompt'])
    model['completion'] = evaluate_cost(model['completion'])
    MODELS.append(model)

# Prompt template
PROMPT_TEMPLATE = CONFIG['prompt_template']

# Date and time formats
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H-%M'

# Other constants
MAX_RETRIES = CONFIG['max_retries']
INITIAL_DELAY = CONFIG['initial_delay']
MAX_DELAY = CONFIG['max_delay']
BACKOFF_MULTIPLIER = CONFIG['backoff_multiplier']
VALID_ANSWERS = CONFIG['valid_answers']