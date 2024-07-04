import os
import yaml
from typing import Dict, Any

# File paths
SCRIPTS_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_FOLDER = os.path.dirname(SCRIPTS_FOLDER)
LOGS_FOLDER = os.path.join(BASE_FOLDER, 'Logs')
CONFIG_PATH = os.path.join(SCRIPTS_FOLDER, 'config.yaml')

# Load configuration
with open(CONFIG_PATH, 'r') as config_file:
    CONFIG: Dict[str, Any] = yaml.safe_load(config_file)

# Database settings
DATABASE_NAME = CONFIG['database']['name']
DATABASE_FOLDER = CONFIG['database']['folder']
DATABASE_PATH = os.path.join(BASE_FOLDER, DATABASE_FOLDER, DATABASE_NAME)

# Vertex API settings
PROJECT_ID = "gen-lang-client-0130870695"
LOCATION = "europe-west2"

# Model definitions
MODELS = CONFIG['models']

# Prompt template
PROMPT_TEMPLATE = CONFIG['prompt_template']

# Date and time formats
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H-%M'

# Other constants
MAX_RETRIES = CONFIG['max_retries']
VALID_ANSWERS = CONFIG['valid_answers']