import os
from typing import Tuple, Optional, Any
from openai import OpenAI
import anthropic
import vertexai
from vertexai.generative_models import GenerativeModel
from together import Together

from src.logger import get_logger
from src.constants import PROJECT_ID, LOCATION, MAX_RETRIES

logger = get_logger()

# Initialize API clients
GPT_client = None
claude_client = None
together_client = None

def initialize_clients() -> None:
    global GPT_client, claude_client, together_client
    if GPT_client is None:
        GPT_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    if claude_client is None:
        claude_client = anthropic.Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))
    if together_client is None:
        together_client = Together(api_key=os.getenv('TOGETHER_API_KEY'))

    vertexai.init(project=PROJECT_ID, location=LOCATION)

def query_language_model(provider: str, model: str, prompt: str, retry_count: int = MAX_RETRIES) -> Tuple[str, int, int]:
    """
    Query a language model with the given prompt.
    
    Args:
    provider (str): The provider of the language model (e.g., 'OpenAI', 'Anthropic')
    model (str): The specific model to use
    prompt (str): The prompt to send to the model
    retry_count (int): Number of times to retry in case of failure
    
    Returns:
    Tuple[str, int, int]: (answer, prompt_tokens, completion_tokens)
    """
    initialize_clients()  # Ensure clients are initialized

    if retry_count == 0:
        return None, 0, 0

    try:
        if provider == 'OpenAI':
            response = GPT_client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}])
            return response.choices[0].message.content.strip(), response.usage.prompt_tokens, response.usage.completion_tokens
        elif provider == 'Anthropic':
            response = claude_client.messages.create(model=model, max_tokens=1024, messages=[{"role": "user", "content": prompt}])
            return response.content[0].text, response.usage.input_tokens, response.usage.output_tokens
        elif provider == 'Google':
            model_instance = GenerativeModel(model)
            response = model_instance.generate_content(prompt)
            return response.text, model_instance.count_tokens(prompt).total_tokens, model_instance.count_tokens(response.text).total_tokens
        elif provider in ['Meta', 'Mistral']:
            response = together_client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}])
            return response.choices[0].message.content, response.usage.prompt_tokens, response.usage.completion_tokens
    except Exception as e:
        print(f"Error during API call: {e}")
        return query_language_model(provider, model, prompt, retry_count - 1)

    return None, 0, 0