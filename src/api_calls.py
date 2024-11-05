import os
import time
import random
from typing import Tuple, Optional, Any, cast
from openai import OpenAI
from openai.types.chat import ChatCompletion
from openai.types.completion_usage import CompletionUsage
import anthropic # type: ignore
from google.oauth2 import service_account
import vertexai  # type: ignore
from vertexai.generative_models import GenerativeModel  # type: ignore
from together import Together  # type: ignore
from mistralai.client import MistralClient # type: ignore
from mistralai.models.chat_completion import ChatMessage # type: ignore

from src.logger import get_logger
from src.constants import PROJECT_ID, LOCATION, SERVICE_ACCOUNT_FILE, MAX_RETRIES, INITIAL_DELAY, MAX_DELAY, BACKOFF_MULTIPLIER

logger = get_logger()

# Initialize API clients
GPT_client = None
claude_client = None
together_client = None
mistral_client = None

def initialize_clients() -> None:
    global GPT_client, claude_client, together_client, mistral_client
    openai_key = os.getenv('OPENAI_API_KEY')
    claude_key = os.getenv('CLAUDE_API_KEY')
    together_key = os.getenv('TOGETHER_API_KEY')
    mistral_key = os.getenv('MISTRAL_API_KEY')

    if not all([openai_key, claude_key, together_key, mistral_key]):
        raise Exception("One or more API keys are missing. Please check your environment variables.")

    if GPT_client is None:
        GPT_client = OpenAI(api_key=openai_key)
    if claude_client is None:
        claude_client = anthropic.Anthropic(api_key=claude_key)
    if together_client is None:
        together_client = Together(api_key=together_key)
    if mistral_client is None:
        mistral_client = MistralClient(api_key=mistral_key)

    # Authenticate using the service account
    CREDENTIALS = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

    vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=CREDENTIALS)

def query_language_model(provider: str, model: str, prompt: str, retry_count: int = MAX_RETRIES) -> Tuple[Optional[str], int, int]:
    """
    Query a language model with the given prompt.
    
    Args:
    provider (str): The provider of the language model (e.g., 'OpenAI', 'Anthropic')
    model (str): The specific model to use
    prompt (str): The prompt to send to the model
    retry_count (int): Number of retries allowed in case of failure

    Returns:
    Tuple[Optional[str], int, int]: The response content, number of tokens in the prompt, and number of tokens in the response
    """
    initial_delay = INITIAL_DELAY
    max_delay = MAX_DELAY
    multiplier = BACKOFF_MULTIPLIER

    initialize_clients()
    
    while retry_count > 0:
        try:
            if provider == 'OpenAI' and GPT_client is not None:
                params = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                }
                response: ChatCompletion = GPT_client.chat.completions.create(**params)
                content = response.choices[0].message.content if hasattr(response, 'choices') and response.choices else None
                usage = response.usage if hasattr(response, 'usage') else None
                return (
                    content,
                    getattr(usage, 'prompt_tokens', 0) if usage else 0,
                    getattr(usage, 'completion_tokens', 0) if usage else 0
                )
            elif provider == 'Anthropic' and claude_client is not None:
                response_anthropic: Any = claude_client.messages.create(model=model, messages=[{"role": "user", "content": prompt}], max_tokens=300)
                content = response_anthropic.content[0].text if response_anthropic.content else None
                usage = response_anthropic.usage if hasattr(response_anthropic, 'usage') else None
                return (
                    content,
                    getattr(usage, 'input_tokens', 0) if usage else 0,
                    getattr(usage, 'output_tokens', 0) if usage else 0
                )
            elif provider == 'Google':
                model_instance = GenerativeModel(model)
                response_google: Any = model_instance.generate_content(prompt)
                return (
                    str(response_google.text) if hasattr(response_google, 'text') and response_google.text is not None else None,
                    int(model_instance.count_tokens(prompt).total_tokens) if hasattr(model_instance, 'count_tokens') else 0,
                    int(model_instance.count_tokens(str(response_google.text) if hasattr(response_google, 'text') and response_google.text is not None else "").total_tokens) if hasattr(model_instance, 'count_tokens') else 0
                )
            elif provider in ['Meta', 'Mistral'] and together_client is not None:
                response_together: Any = together_client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}])
                content = response_together.choices[0].message.content if hasattr(response_together, 'choices') and response_together.choices else None
                usage = response_together.usage if hasattr(response_together, 'usage') else None
                return (
                    content,
                    getattr(usage, 'prompt_tokens', 0) if usage else 0,
                    getattr(usage, 'completion_tokens', 0) if usage else 0
                )
            elif provider == 'MistralM':
                response_mistral: Any = mistral_client.chat(model=model, messages=[ChatMessage(role="user", content=prompt)])
                content = response_mistral.choices[0].message.content if response_mistral.choices else None
                usage = response_mistral.usage if hasattr(response_mistral, 'usage') else None
                return (
                    content,
                    getattr(usage, 'input_tokens', 0) if usage else 0,
                    getattr(usage, 'output_tokens', 0) if usage else 0
                )
        except Exception as e:
            logger.error(f"Error during API call: {e}")
            retry_count -= 1
            if retry_count > 0:
                delay = min(max_delay, initial_delay * (multiplier ** (MAX_RETRIES - retry_count))) + random.uniform(0, 1)
                logger.info(f"Retrying in {delay:.2f} seconds...")
                time.sleep(delay)
            else:
                logger.error("Maximum retries reached. Returning no result.")
                break

    return None, 0, 0