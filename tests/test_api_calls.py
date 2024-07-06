import unittest
from unittest.mock import patch, MagicMock
from src.api_calls import query_language_model, initialize_clients

class TestApiCalls(unittest.TestCase):

    @patch('src.api_calls.os.getenv')
    def test_initialize_clients(self, mock_getenv):
        mock_getenv.side_effect = lambda x: 'dummy_key' if x in ['OPENAI_API_KEY', 'CLAUDE_API_KEY', 'TOGETHER_API_KEY'] else None
        
        with patch('src.api_calls.OpenAI') as mock_openai, \
             patch('src.api_calls.anthropic.Anthropic') as mock_anthropic, \
             patch('src.api_calls.Together') as mock_together, \
             patch('src.api_calls.vertexai.init') as mock_vertexai_init:
            
            initialize_clients()
            
            mock_openai.assert_called_once_with(api_key='dummy_key')
            mock_anthropic.assert_called_once_with(api_key='dummy_key')
            mock_together.assert_called_once_with(api_key='dummy_key')
            mock_vertexai_init.assert_called_once()

    @patch('src.api_calls.GPT_client')
    @patch('src.api_calls.claude_client')
    @patch('src.api_calls.together_client')
    @patch('src.api_calls.GenerativeModel')
    def test_query_language_model_all_providers(self, mock_generative_model, mock_together, mock_claude, mock_gpt):
        # Test OpenAI
        mock_gpt.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="OpenAI response"))],
            usage=MagicMock(prompt_tokens=10, completion_tokens=5)
        )
        response, prompt_tokens, completion_tokens = query_language_model('OpenAI', 'gpt-4', 'Test prompt')
        self.assertEqual(response, "OpenAI response")
        self.assertEqual(prompt_tokens, 10)
        self.assertEqual(completion_tokens, 5)

        # Test Anthropic
        mock_claude.messages.create.return_value = MagicMock(
            content=[MagicMock(text="Anthropic response")],
            usage=MagicMock(input_tokens=10, output_tokens=5)
        )
        response, prompt_tokens, completion_tokens = query_language_model('Anthropic', 'claude-3', 'Test prompt')
        self.assertEqual(response, "Anthropic response")
        self.assertEqual(prompt_tokens, 10)
        self.assertEqual(completion_tokens, 5)

        # Test Google
        mock_generative_model.return_value.generate_content.return_value = MagicMock(text="Google response")
        mock_generative_model.return_value.count_tokens.return_value = MagicMock(total_tokens=15)
        response, prompt_tokens, completion_tokens = query_language_model('Google', 'gemini-pro', 'Test prompt')
        self.assertEqual(response, "Google response")
        self.assertEqual(prompt_tokens, 15)
        self.assertEqual(completion_tokens, 15)

        # Test Meta/Mistral
        mock_together.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Together response"))],
            usage=MagicMock(prompt_tokens=10, completion_tokens=5)
        )
        response, prompt_tokens, completion_tokens = query_language_model('Meta', 'llama-2', 'Test prompt')
        self.assertEqual(response, "Together response")
        self.assertEqual(prompt_tokens, 10)
        self.assertEqual(completion_tokens, 5)

    @patch('src.api_calls.GPT_client')
    @patch('src.api_calls.claude_client')
    @patch('src.api_calls.together_client')
    @patch('src.api_calls.GenerativeModel')
    def test_query_language_model_retry(self, mock_generative_model, mock_together, mock_claude, mock_gpt):
        mock_gpt.chat.completions.create.side_effect = [Exception("API Error"), MagicMock(
            choices=[MagicMock(message=MagicMock(content="OpenAI response"))],
            usage=MagicMock(prompt_tokens=10, completion_tokens=5)
        )]
        
        response, prompt_tokens, completion_tokens = query_language_model('OpenAI', 'gpt-4', 'Test prompt')
        self.assertEqual(response, "OpenAI response")
        self.assertEqual(prompt_tokens, 10)
        self.assertEqual(completion_tokens, 5)
        self.assertEqual(mock_gpt.chat.completions.create.call_count, 2)

    @patch('src.api_calls.GPT_client')
    @patch('src.api_calls.claude_client')
    @patch('src.api_calls.together_client')
    @patch('src.api_calls.GenerativeModel')
    def test_query_language_model_all_retries_failed(self, mock_generative_model, mock_together, mock_claude, mock_gpt):
        mock_gpt.chat.completions.create.side_effect = Exception("API Error")
        
        response, prompt_tokens, completion_tokens = query_language_model('OpenAI', 'gpt-4', 'Test prompt')
        self.assertIsNone(response)
        self.assertEqual(prompt_tokens, 0)
        self.assertEqual(completion_tokens, 0)
        self.assertEqual(mock_gpt.chat.completions.create.call_count, 3)  # Assuming MAX_RETRIES is 3

    @patch('src.api_calls.GPT_client')
    @patch('src.api_calls.claude_client')
    @patch('src.api_calls.together_client')
    @patch('src.api_calls.GenerativeModel')
    def test_query_language_model_unknown_provider(self, mock_generative_model, mock_together, mock_claude, mock_gpt):
        response, prompt_tokens, completion_tokens = query_language_model('UnknownProvider', 'unknown-model', 'Test prompt')
        self.assertIsNone(response)
        self.assertEqual(prompt_tokens, 0)
        self.assertEqual(completion_tokens, 0)

if __name__ == '__main__':
    unittest.main()