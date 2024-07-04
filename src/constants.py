import os

# Database
DATABASE_NAME = 'results_database.sqlite'
DATABASE_FOLDER = 'Database'

# Date and time formats
DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H-%M'

# File paths
SCRIPTS_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_FOLDER = os.path.dirname(SCRIPTS_FOLDER)
LOGS_FOLDER = os.path.join(BASE_FOLDER, 'Logs')

# Database path
DATABASE_PATH = os.path.join(BASE_FOLDER, DATABASE_FOLDER, DATABASE_NAME)

# API related
PROJECT_ID = "gen-lang-client-0130870695"
LOCATION = "europe-west2"

# Model definitions
MODELS = [
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

# Prompt template
PROMPT_TEMPLATE = """Choose the correct answer for the following marketing multiple-choice question. ANSWER ONLY with a SINGLE letter of the correct choice. DO NOT give an explanation.

Question: {question}
Choices:
A. {option_a}
B. {option_b}
C. {option_c}
D. {option_d}
Answer:"""

# Other constants
MAX_RETRIES = 3
VALID_ANSWERS = ['A', 'B', 'C', 'D']