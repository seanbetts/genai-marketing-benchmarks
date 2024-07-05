import unittest
from unittest.mock import patch
from src.user_interface import get_user_inputs, confirm_run

class TestUserInterface(unittest.TestCase):

    @patch('builtins.input')
    def test_get_user_inputs(self, mock_input):
        mock_input.side_effect = ['100', '2']
        num_questions, num_rounds = get_user_inputs()
        self.assertEqual(num_questions, 100)
        self.assertEqual(num_rounds, 2)

        mock_input.side_effect = ['all', '3']
        num_questions, num_rounds = get_user_inputs()
        self.assertEqual(num_questions, 'all')
        self.assertEqual(num_rounds, 3)

    @patch('builtins.input')
    def test_confirm_run(self, mock_input):
        mock_input.return_value = 'y'
        result = confirm_run(10.0, [('Model1', 5.0), ('Model2', 5.0)], 2, 100, 200)
        self.assertTrue(result)

        mock_input.return_value = 'n'
        result = confirm_run(10.0, [('Model1', 5.0), ('Model2', 5.0)], 2, 100, 200)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()