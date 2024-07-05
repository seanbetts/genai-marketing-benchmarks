import unittest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from src.cli import run_benchmark
import pandas as pd
from datetime import datetime

class TestCLI(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    @patch('src.cli.os.getenv')
    @patch('src.cli.select_models')
    @patch('src.cli.load_questions')
    @patch('src.cli.select_categories')
    @patch('src.cli.get_user_inputs')
    @patch('src.cli.estimate_cost')
    @patch('src.cli.confirm_run')
    @patch('src.cli.check_table_exists_and_get_highest_round')
    @patch('src.cli.query_language_model')
    @patch('src.cli.save_results_to_sqlite')
    @patch('src.cli.answer_check')
    def test_run_benchmark_interactive(self, mock_answer_check, mock_save, mock_query, mock_check_table, mock_confirm, mock_estimate, 
                                       mock_get_inputs, mock_select_categories, mock_load_questions, mock_select_models, mock_getenv):
        # Mock environment variables
        mock_getenv.return_value = 'mock_api_key'
        
        # Mock the interactive mode selections
        mock_select_models.return_value = [{'name': 'TestModel', 'provider': 'TestProvider', 'variant': 'TestVariant'}]
        mock_load_questions.return_value = pd.DataFrame({
            'Category': ['TestCategory'], 
            'Question': ['TestQuestion'],
            'Discipline': ['TestDiscipline'],
            'Sub_Category': ['TestSubCategory'],
            'Question_Code': ['TestCode'],
            'Correct_Option': ['A'],
            'Option_A': ['A'],
            'Option_B': ['B'],
            'Option_C': ['C'],
            'Option_D': ['D']
        })
        mock_select_categories.return_value = ['TestCategory']
        mock_get_inputs.return_value = ('all', 1)
        mock_estimate.return_value = (10.0, [('TestModel', 10.0)])
        mock_confirm.return_value = True
        mock_check_table.return_value = 0
        mock_query.return_value = ('A', 10, 5)
        mock_answer_check.return_value = ('A', True)

        result = self.runner.invoke(run_benchmark)
        
        print(f"Exit code: {result.exit_code}")
        print(f"Exception: {result.exception}")
        print(f"Output: {result.output}")
        
        self.assertEqual(result.exit_code, 0)
        mock_select_models.assert_called_once()
        mock_load_questions.assert_called_once()
        mock_select_categories.assert_called_once()
        mock_get_inputs.assert_called_once()
        mock_estimate.assert_called_once()
        mock_confirm.assert_called_once()
        mock_check_table.assert_called_once()
        mock_query.assert_called()
        mock_save.assert_called()

    @patch('src.cli.os.getenv')
    @patch('src.cli.load_questions')
    @patch('src.cli.estimate_cost')
    @patch('src.cli.check_table_exists_and_get_highest_round')
    @patch('src.cli.query_language_model')
    @patch('src.cli.save_results_to_sqlite')
    @patch('src.cli.answer_check')
    def test_run_benchmark_non_interactive(self, mock_answer_check, mock_save, mock_query, mock_check_table, mock_estimate, mock_load_questions, mock_getenv):
        # Mock environment variables
        mock_getenv.return_value = 'mock_api_key'
        
        mock_load_questions.return_value = pd.DataFrame({
            'Category': ['TestCategory'], 
            'Question': ['TestQuestion'],
            'Discipline': ['TestDiscipline'],
            'Sub_Category': ['TestSubCategory'],
            'Question_Code': ['TestCode'],
            'Correct_Option': ['A'],
            'Option_A': ['A'],
            'Option_B': ['B'],
            'Option_C': ['C'],
            'Option_D': ['D']
        })
        mock_estimate.return_value = (10.0, [('TestModel', 10.0)])
        mock_check_table.return_value = 0
        mock_query.return_value = ('A', 10, 5)
        mock_answer_check.return_value = ('A', True)

        result = self.runner.invoke(run_benchmark, [
            '--non-interactive',
            '--num-questions', '1',
            '--num-rounds', '1',
            '--models', 'TestModel',
            '--categories', 'TestCategory'
        ])
        
        print(f"Exit code: {result.exit_code}")
        print(f"Exception: {result.exception}")
        print(f"Output: {result.output}")
        
        self.assertEqual(result.exit_code, 0)
        mock_load_questions.assert_called_once()
        mock_estimate.assert_called_once()
        mock_check_table.assert_called_once()
        mock_query.assert_called()
        mock_save.assert_called()

if __name__ == '__main__':
    unittest.main()