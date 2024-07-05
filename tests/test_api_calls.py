import unittest
from unittest.mock import patch, MagicMock
from src.api_calls import query_language_model, initialize_clients

class TestApiCalls(unittest.TestCase):

    @patch('src.api_calls.GPT_client')
    @patch('src.api_calls.claude_client')
    @patch('src.api_calls.together_client')
    @patch('src.api_calls.GenerativeModel')
    
    def test_query_language_model(self, mock_generative_model, mock_together, mock_claude, mock_gpt):
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

    @patch('src.api_calls.OpenAI')
    @patch('src.api_calls.anthropic.Anthropic')
    @patch('src.api_calls.Together')
    @patch('src.api_calls.vertexai.init')

    def test_initialize_clients(self, mock_vertexai_init, mock_together, mock_anthropic, mock_openai):
        initialize_clients()
        mock_openai.assert_called_once()
        mock_anthropic.assert_called_once()
        mock_together.assert_called_once()
        mock_vertexai_init.assert_called_once()

if __name__ == '__main__':
    unittest.main()