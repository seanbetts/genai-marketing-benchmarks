import unittest
from unittest.mock import patch, mock_open
import yaml
from src.constants import evaluate_cost, CONFIG, MODELS, PROMPT_TEMPLATE, MAX_RETRIES, VALID_ANSWERS

class TestConstants(unittest.TestCase):

    def test_evaluate_cost_valid(self):
        self.assertEqual(evaluate_cost("10 / 1000000"), 0.00001)
        self.assertEqual(evaluate_cost("5 + 5"), 10)

    def test_evaluate_cost_invalid(self):
        with patch('builtins.print') as mock_print:
            result = evaluate_cost("invalid_expression")
            self.assertEqual(result, 0.0)
            mock_print.assert_called_once()

    @patch('yaml.safe_load')
    def test_config_loading(self, mock_yaml_load):
        mock_config = {
            'database': {'name': 'test.db', 'folder': 'TestDB'},
            'api': {'project_id': 'test_project', 'location': 'test_location'},
            'models': [
                {'name': 'TestModel', 'prompt': '10 / 1000000', 'completion': '20 / 1000000'}
            ],
            'prompt_template': 'Test template',
            'max_retries': 3,
            'valid_answers': ['A', 'B', 'C', 'D']
        }
        mock_yaml_load.return_value = mock_config

        # Re-import the constants module to trigger config loading
        with patch('builtins.open', mock_open(read_data='')):
            import importlib
            import src.constants
            importlib.reload(src.constants)

        self.assertEqual(src.constants.CONFIG, mock_config)
        self.assertEqual(len(src.constants.MODELS), 1)
        self.assertEqual(src.constants.MODELS[0]['prompt'], 0.00001)
        self.assertEqual(src.constants.MODELS[0]['completion'], 0.00002)
        self.assertEqual(src.constants.PROMPT_TEMPLATE, 'Test template')
        self.assertEqual(src.constants.MAX_RETRIES, 3)
        self.assertEqual(src.constants.VALID_ANSWERS, ['A', 'B', 'C', 'D'])

if __name__ == '__main__':
    unittest.main()