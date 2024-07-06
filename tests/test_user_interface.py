import unittest
from unittest.mock import patch, MagicMock
from src.user_interface import get_user_inputs, confirm_run, clear_console, curses_menu, select_models, select_categories

# Mock curses module in case it's not available
try:
    import curses
except ImportError:
    curses = MagicMock()
    curses.KEY_DOWN = 258
    curses.KEY_UP = 259

# Mock curses module
mock_curses = MagicMock()
mock_curses.KEY_DOWN = 258
mock_curses.KEY_UP = 259
mock_curses.A_REVERSE = 65536

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

    @patch('os.system')
    def test_clear_console(self, mock_system):
        clear_console()
        mock_system.assert_called_once()

    @patch('src.user_interface.curses.wrapper')
    def test_select_models(self, mock_wrapper):
        mock_wrapper.return_value = ['Model1 (Provider: Provider1)', 'Model2 (Provider: Provider2)']
        models = [
            {'name': 'Model1', 'provider': 'Provider1'},
            {'name': 'Model2', 'provider': 'Provider2'},
            {'name': 'Model3', 'provider': 'Provider3'}
        ]
        selected = select_models(models)
        self.assertEqual(len(selected), 2)
        self.assertEqual(selected[0]['name'], 'Model1')
        self.assertEqual(selected[1]['name'], 'Model2')

    @patch('src.user_interface.curses.wrapper')
    def test_select_categories(self, mock_wrapper):
        mock_wrapper.return_value = ['Category1', 'Category3']
        categories = ['Category1', 'Category2', 'Category3']
        selected = select_categories(categories)
        self.assertEqual(selected, ['Category1', 'Category3'])

    @patch('src.user_interface.curses', mock_curses)
    def test_curses_menu(self):
        mock_stdscr = MagicMock()
        mock_stdscr.getch.side_effect = [
            mock_curses.KEY_DOWN,
            ord(' '),
            mock_curses.KEY_UP,
            10  # Enter key
        ]
        items = ['Item1', 'Item2', 'Item3']
        result = curses_menu(mock_stdscr, items, "Test Prompt", all_selected=False)
        self.assertEqual(result, ['Item2'])
        mock_stdscr.clear.assert_called()
        mock_stdscr.refresh.assert_called()
        mock_stdscr.addstr.assert_called()

if __name__ == '__main__':
    unittest.main()