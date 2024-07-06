import unittest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
import pandas as pd
from src.cli import run_benchmark

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch('src.cli.load_questions')
    @patch('src.cli.query_language_model')
    @patch('src.cli.save_results_to_sqlite')
    @patch('src.cli.os.getenv')
    def test_run_benchmark_interactive(self, mock_getenv, mock_save_results, mock_query_model, mock_load_questions):
        mock_getenv.side_effect = lambda x: 'dummy_key' if x in ['OPENAI_API_KEY', 'CLAUDE_API_KEY', 'TOGETHER_API_KEY'] else None
        mock_load_questions.return_value = pd.DataFrame({
            'Discipline': ['Marketing'],
            'Category': ['Test Category'],
            'Question': ['Test Question'],
            'Option_A': ['A'],
            'Option_B': ['B'],
            'Option_C': ['C'],
            'Option_D': ['D'],
            'Correct_Option': ['A'],
            'Question_Code': ['TEST001']
        })
        mock_query_model.return_value = ('A', 10, 5)
        
        with patch('src.cli.select_models', return_value=[{'name': 'Test Model', 'provider': 'Test Provider', 'variant': 'test-variant', 'prompt': 0.01, 'completion': 0.01}]), \
             patch('src.cli.select_categories', return_value=['Test Category']), \
             patch('src.cli.get_user_inputs', return_value=(1, 1)), \
             patch('src.cli.confirm_run', return_value=True):
            
            result = self.runner.invoke(run_benchmark, ['--interactive'])
            
            print(f"Interactive test output: {result.output}")
            self.assertEqual(result.exit_code, 0, f"Interactive test failed with output: {result.output}")
            mock_save_results.assert_called()

    @patch('src.cli.load_questions')
    @patch('src.cli.query_language_model')
    @patch('src.cli.save_results_to_sqlite')
    @patch('src.cli.os.getenv')
    def test_run_benchmark_non_interactive(self, mock_getenv, mock_save_results, mock_query_model, mock_load_questions):
        mock_getenv.side_effect = lambda x: 'dummy_key' if x in ['OPENAI_API_KEY', 'CLAUDE_API_KEY', 'TOGETHER_API_KEY'] else None
        mock_load_questions.return_value = pd.DataFrame({
            'Discipline': ['SEO'],
            'Category': ['SEO'],
            'Question': ['Test Question'],
            'Option_A': ['A'],
            'Option_B': ['B'],
            'Option_C': ['C'],
            'Option_D': ['D'],
            'Correct_Option': ['A'],
            'Question_Code': ['SEO001']
        })
        mock_query_model.return_value = ('A', 10, 5)
        
        with patch('src.cli.MODELS', [{'name': 'GPT-4', 'provider': 'OpenAI', 'variant': 'gpt-4', 'prompt': 0.01, 'completion': 0.01}]):
            result = self.runner.invoke(run_benchmark, [
                '--non-interactive',
                '--num-questions', '1',
                '--num-rounds', '1',
                '--models', 'GPT-4',
                '--categories', 'SEO'
            ])
            
            print(f"Non-interactive test output: {result.output}")
            self.assertEqual(result.exit_code, 0, f"Non-interactive test failed with output: {result.output}")
            mock_save_results.assert_called()

    @patch('src.cli.load_questions')
    @patch('src.cli.query_language_model')
    @patch('src.cli.save_results_to_sqlite')
    @patch('src.cli.os.getenv')
    def test_run_benchmark_all_questions(self, mock_getenv, mock_save_results, mock_query_model, mock_load_questions):
        mock_getenv.side_effect = lambda x: 'dummy_key' if x in ['OPENAI_API_KEY', 'CLAUDE_API_KEY', 'TOGETHER_API_KEY'] else None
        mock_load_questions.return_value = pd.DataFrame({
            'Discipline': ['SEO'] * 100,
            'Category': ['SEO'] * 100,
            'Question': ['Q'] * 100,
            'Option_A': ['A'] * 100,
            'Option_B': ['B'] * 100,
            'Option_C': ['C'] * 100,
            'Option_D': ['D'] * 100,
            'Correct_Option': ['A'] * 100,
            'Question_Code': [f'SEO{i:03d}' for i in range(1, 101)]
        })
        mock_query_model.return_value = ('A', 10, 5)
        
        with patch('src.cli.MODELS', [{'name': 'GPT-4', 'provider': 'OpenAI', 'variant': 'gpt-4', 'prompt': 0.01, 'completion': 0.01}]):
            result = self.runner.invoke(run_benchmark, [
                '--non-interactive',
                '--num-questions', 'all',
                '--num-rounds', '1',
                '--models', 'GPT-4',
                '--categories', 'SEO'
            ])
            
            print(f"All questions test output: {result.output}")
            self.assertEqual(result.exit_code, 0, f"All questions test failed with output: {result.output}")
            mock_save_results.assert_called()

    @patch('src.cli.os.getenv')
    def test_missing_api_keys(self, mock_getenv):
        mock_getenv.return_value = None
        result = self.runner.invoke(run_benchmark, ['--interactive'])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("is not set in the environment variables", result.output)

    @patch('src.cli.load_questions')
    @patch('src.cli.os.getenv')
    def test_no_models_selected(self, mock_getenv, mock_load_questions):
        mock_getenv.side_effect = lambda x: 'dummy_key' if x in ['OPENAI_API_KEY', 'CLAUDE_API_KEY', 'TOGETHER_API_KEY'] else None
        mock_load_questions.return_value = pd.DataFrame({'Category': ['Test']})
        with patch('src.cli.select_models', return_value=[]), \
             patch('src.cli.select_categories', return_value=['Test']), \
             patch('src.cli.get_user_inputs', return_value=(1, 1)):
            result = self.runner.invoke(run_benchmark, ['--interactive'])
            self.assertNotEqual(result.exit_code, 0)
            self.assertIn("No models selected", result.output)

    @patch('src.cli.load_questions')
    @patch('src.cli.os.getenv')
    def test_no_categories_selected(self, mock_getenv, mock_load_questions):
        mock_getenv.side_effect = lambda x: 'dummy_key' if x in ['OPENAI_API_KEY', 'CLAUDE_API_KEY', 'TOGETHER_API_KEY'] else None
        mock_load_questions.return_value = pd.DataFrame({'Category': ['Test']})
        with patch('src.cli.select_models', return_value=[{'name': 'Test Model'}]), \
             patch('src.cli.select_categories', return_value=[]), \
             patch('src.cli.get_user_inputs', return_value=(1, 1)):
            result = self.runner.invoke(run_benchmark, ['--interactive'])
            self.assertNotEqual(result.exit_code, 0)
            self.assertIn("No categories selected", result.output)

    @patch('src.cli.load_questions')
    @patch('src.cli.os.getenv')
    def test_no_questions_available(self, mock_getenv, mock_load_questions):
        mock_getenv.side_effect = lambda x: 'dummy_key' if x in ['OPENAI_API_KEY', 'CLAUDE_API_KEY', 'TOGETHER_API_KEY'] else None
        mock_load_questions.return_value = pd.DataFrame({'Category': []})
        with patch('src.cli.select_models', return_value=[{'name': 'Test Model'}]), \
             patch('src.cli.select_categories', return_value=['Test']), \
             patch('src.cli.get_user_inputs', return_value=(1, 1)):
            result = self.runner.invoke(run_benchmark, ['--interactive'])
            self.assertNotEqual(result.exit_code, 0)
            self.assertIn("No questions available for the selected categories", result.output)

    @patch('src.cli.load_questions')
    @patch('src.cli.os.getenv')
    def test_user_abort(self, mock_getenv, mock_load_questions):
        mock_getenv.side_effect = lambda x: 'dummy_key' if x in ['OPENAI_API_KEY', 'CLAUDE_API_KEY', 'TOGETHER_API_KEY'] else None
        mock_load_questions.return_value = pd.DataFrame({'Category': ['Test']})
        with patch('src.cli.select_models', return_value=[{'name': 'Test Model', 'provider': 'Test', 'variant': 'test'}]), \
            patch('src.cli.select_categories', return_value=['Test']), \
            patch('src.cli.get_user_inputs', return_value=(1, 1)), \
            patch('src.cli.confirm_run', return_value=False), \
            patch('src.cli.estimate_cost', return_value=(0, [])):
            result = self.runner.invoke(run_benchmark, ['--interactive'])
            self.assertEqual(result.exit_code, 0, f"Expected exit code 0, but got {result.exit_code}. Output: {result.output}")
            self.assertIn("Testing run aborted by the user", result.output)

if __name__ == '__main__':
    unittest.main()