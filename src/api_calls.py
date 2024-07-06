import os
from typing import Tuple, Optional, Any, cast
from openai import OpenAI
from openai.types.chat import ChatCompletion
from openai.types.completion_usage import CompletionUsage
import anthropic # type: ignore
import vertexai  # type: ignore
from vertexai.generative_models import GenerativeModel  # type: ignore
from together import Together  # type: ignore

from src.logger import get_logger
from src.constants import PROJECT_ID, LOCATION, MAX_RETRIES

logger = get_logger()

# Initialize API clients
GPT_client = None
claude_client = None
together_client = None

def initialize_clients() -> None:
    global GPT_client, claude_client, together_client
    openai_key = os.getenv('OPENAI_API_KEY')
    claude_key = os.getenv('CLAUDE_API_KEY')
    together_key = os.getenv('TOGETHER_API_KEY')

    if not all([openai_key, claude_key, together_key]):
        raise Exception("One or more API keys are missing. Please check your environment variables.")

    if GPT_client is None:
        GPT_client = OpenAI(api_key=openai_key)
    if claude_client is None:
        claude_client = anthropic.Anthropic(api_key=claude_key)
    if together_client is None:
        together_client = Together(api_key=together_key)

    vertexai.init(project=PROJECT_ID, location=LOCATION)

def query_language_model(provider: str, model: str, prompt: str, retry_count: int = MAX_RETRIES) -> Tuple[Optional[str], int, int]:
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
        if provider == 'OpenAI' and GPT_client is not None:
            response_openai: ChatCompletion = GPT_client.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}])
            content = response_openai.choices[0].message.content if response_openai.choices else None
            usage: Optional[CompletionUsage] = response_openai.usage
            return (
                content.strip() if content else None,
                usage.prompt_tokens if usage and usage.prompt_tokens is not None else 0,
                usage.completion_tokens if usage and usage.completion_tokens is not None else 0
            )
        elif provider == 'Anthropic' and claude_client is not None:
            response_anthropic: Any = claude_client.messages.create(model=model, max_tokens=1024, messages=[{"role": "user", "content": prompt}])
            content = response_anthropic.content[0].text if hasattr(response_anthropic, 'content') and response_anthropic.content else None
            usage = response_anthropic.usage if hasattr(response_anthropic, 'usage') else None
            return (
                content,
                getattr(usage, 'input_tokens', 0) if usage else 0,
                getattr(usage, 'output_tokens', 0) if usage else 0
            )
        elif provider == 'Google':
            model_instance: Any = GenerativeModel(model)
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
    except Exception as e:
        print(f"Error during API call: {e}")
        return query_language_model(provider, model, prompt, retry_count - 1)

    return None, 0, 0