import unittest
import pandas as pd
import os
import sqlite3
from unittest.mock import patch, MagicMock
from src.data_processing import (
    estimate_cost,
    calculate_token_cost,
    load_questions,
    answer_check,
    check_table_exists_and_get_highest_round,
    sanitize_column_name,
    save_results_to_sqlite,
    get_sqlite_type,
    ensure_summary_table
)

class TestDataProcessing(unittest.TestCase):

    @patch('sqlite3.connect')
    def test_load_questions_file_not_found(self, mock_connect):
        mock_connect.side_effect = FileNotFoundError("Database file not found")
        with self.assertRaises(FileNotFoundError):
            load_questions('non_existent_path.db')

    @patch('sqlite3.connect')
    def test_check_table_exists_and_get_highest_round_table_exists(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ('existing_table',)
        mock_cursor.fetchone.return_value = (5,)  # Highest round number
        mock_connect.return_value.cursor.return_value = mock_cursor

        result = check_table_exists_and_get_highest_round('test_model', '2023-01-01')
        self.assertEqual(result, 5)

    @patch('sqlite3.connect')
    def test_check_table_exists_and_get_highest_round_table_not_exists(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_connect.return_value.cursor.return_value = mock_cursor

        result = check_table_exists_and_get_highest_round('test_model', '2023-01-01')
        self.assertEqual(result, 0)

    @patch('sqlite3.connect')
    def test_save_results_to_sqlite_new_table(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None  # Table doesn't exist
        mock_connect.return_value.cursor.return_value = mock_cursor

        test_df = pd.DataFrame({
            'Round': [1],
            'Discipline': ['Test'],
            'Category': ['Test'],
            'Is_Correct': [True]
        })

        save_results_to_sqlite(test_df, 'test_model', '2023-01-01')
        
        # Check if CREATE TABLE was called
        create_table_calls = [call for call in mock_cursor.execute.call_args_list if 'CREATE TABLE' in str(call)]
        self.assertTrue(len(create_table_calls) > 0)

    @patch('sqlite3.connect')
    def test_save_results_to_sqlite_existing_table(self, mock_connect):
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ('existing_table',)  # Table exists
        mock_connect.return_value.cursor.return_value = mock_cursor

        test_df = pd.DataFrame({
            'Round': [1],
            'Discipline': ['Test'],
            'Category': ['Test'],
            'Is_Correct': [True],
            'New_Column': ['Value']  # New column to test ALTER TABLE
        })

        save_results_to_sqlite(test_df, 'test_model', '2023-01-01')
        
        # Check if ALTER TABLE was called for the new column
        alter_table_calls = [call for call in mock_cursor.execute.call_args_list if 'ALTER TABLE' in str(call)]
        self.assertTrue(len(alter_table_calls) > 0)

    def test_ensure_summary_table(self):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        # Mock the result of PRAGMA table_info(table_name)
        mock_cursor.fetchall.return_value = [
            (0, 'Model', 'TEXT', 0, None, 0),
            (1, 'Round', 'INTEGER', 0, None, 0),
            (2, 'Date', 'TEXT', 0, None, 0)
        ]

        columns = pd.Index(['Model', 'Round', 'Date', 'New_Column'])
        ensure_summary_table(mock_conn, 'test_summary', columns)

        # Check if CREATE TABLE IF NOT EXISTS was called
        mock_cursor.execute.assert_any_call("CREATE TABLE IF NOT EXISTS test_summary (Model TEXT, Round INTEGER, Date TEXT)")
        
        # Check if ALTER TABLE was called for the new column
        alter_table_calls = [call for call in mock_cursor.execute.call_args_list if 'ALTER TABLE' in str(call)]
        self.assertEqual(len(alter_table_calls), 1)
        mock_cursor.execute.assert_any_call("ALTER TABLE test_summary ADD COLUMN New_Column REAL")

    def test_estimate_cost_empty_models(self):
        total_cost, model_costs = estimate_cost(10, 2, [])
        self.assertEqual(total_cost, 0)
        self.assertEqual(model_costs, [])

    def test_calculate_token_cost_zero_tokens(self):
        model_info = {"prompt": 0.001, "completion": 0.002}
        cost = calculate_token_cost(0, 0, model_info)
        self.assertEqual(cost, 0)

    @patch('os.path.exists')
    def test_load_questions_file_not_found(self, mock_exists):
        mock_exists.return_value = False
        with self.assertRaises(FileNotFoundError):
            load_questions('non_existent_path.db')

    def test_ensure_summary_table_no_new_columns(self):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = [
            (0, 'Model', 'TEXT', 0, None, 0),
            (1, 'Round', 'INTEGER', 0, None, 0),
            (2, 'Date', 'TEXT', 0, None, 0)
        ]

        columns = pd.Index(['Model', 'Round', 'Date'])
        ensure_summary_table(mock_conn, 'test_summary', columns)

        # Check that ALTER TABLE was not called
        alter_table_calls = [call for call in mock_cursor.execute.call_args_list if 'ALTER TABLE' in str(call)]
        self.assertEqual(len(alter_table_calls), 0)

    def test_estimate_cost_with_models(self):
        models = [
            {"name": "Model1", "prompt": 0.001, "completion": 0.002},
            {"name": "Model2", "prompt": 0.002, "completion": 0.003}
        ]
        total_cost, model_costs = estimate_cost(10, 2, models)
        self.assertGreater(total_cost, 0)
        self.assertEqual(len(model_costs), 2)
        for model_name, cost in model_costs:
            self.assertIn(model_name, ["Model1", "Model2"])
            self.assertGreater(cost, 0)

    def test_calculate_token_cost_non_zero(self):
        model_info = {"prompt": 0.001, "completion": 0.002}
        cost = calculate_token_cost(100, 50, model_info)
        self.assertEqual(cost, 0.2)

    @patch('sqlite3.connect')
    @patch('pandas.read_sql_query')
    @patch('os.path.exists')
    def test_load_questions_success(self, mock_exists, mock_read_sql, mock_connect):
        mock_exists.return_value = True
        mock_df = pd.DataFrame({
            'id': [1, 2],
            'Question': ['Question 1', 'Question 2'],
            'Category': ['Category 1', 'Category 2']
        })
        mock_read_sql.return_value = mock_df
        
        df = load_questions('test.db')
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        self.assertEqual(list(df.columns), ['id', 'Question', 'Category'])
        mock_read_sql.assert_called_once()
        mock_connect.assert_called_once_with('test.db')

    def test_ensure_summary_table_with_new_columns(self):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = [
            (0, 'Model', 'TEXT', 0, None, 0),
            (1, 'Round', 'INTEGER', 0, None, 0),
            (2, 'Date', 'TEXT', 0, None, 0)
        ]

        columns = pd.Index(['Model', 'Round', 'Date', 'NewColumn1', 'NewColumn2'])
        ensure_summary_table(mock_conn, 'test_summary', columns)

        # Check that ALTER TABLE was called for new columns
        alter_table_calls = [call for call in mock_cursor.execute.call_args_list if 'ALTER TABLE' in str(call)]
        self.assertEqual(len(alter_table_calls), 2)

    def test_calculate_token_cost_zero_completion(self):
        model_info = {"prompt": 0.001, "completion": 0.002}
        cost = calculate_token_cost(100, 0, model_info)
        self.assertEqual(cost, 0.1)

    @patch('sqlite3.connect')
    @patch('pandas.read_sql_query')
    @patch('os.path.exists')
    def test_load_questions_file_exists_no_data(self, mock_exists, mock_read_sql, mock_connect):
        mock_exists.return_value = True
        mock_read_sql.return_value = pd.DataFrame()
        
        df = load_questions('test.db')
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 0)
        mock_read_sql.assert_called_once()
        mock_connect.assert_called_once_with('test.db')

    def test_ensure_summary_table_with_dict_info(self):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = [
            {'name': 'Model', 'type': 'TEXT'},
            {'name': 'Round', 'type': 'INTEGER'},
            {'name': 'Date', 'type': 'TEXT'}
        ]

        columns = pd.Index(['Model', 'Round', 'Date', 'NewColumn'])
        ensure_summary_table(mock_conn, 'test_summary', columns)

        # Check that ALTER TABLE was called for new column
        alter_table_calls = [call for call in mock_cursor.execute.call_args_list if 'ALTER TABLE' in str(call)]
        self.assertEqual(len(alter_table_calls), 1)

    def test_calculate_token_cost_zero_prompt(self):
        model_info = {"prompt": 0.001, "completion": 0.002}
        cost = calculate_token_cost(0, 100, model_info)
        self.assertEqual(cost, 0.2)

    @patch('sqlite3.connect')
    @patch('pandas.read_sql_query')
    @patch('os.path.exists')
    def test_load_questions_sql_error(self, mock_exists, mock_read_sql, mock_connect):
        mock_exists.return_value = True
        mock_read_sql.side_effect = sqlite3.Error("SQL Error")
        
        with self.assertRaises(sqlite3.Error):
            load_questions('test.db')

    def test_ensure_summary_table_mixed_info(self):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = [
            (0, 'Model', 'TEXT', 0, None, 0),
            {'name': 'Round', 'type': 'INTEGER'},
            (2, 'Date', 'TEXT', 0, None, 0)
        ]

        columns = pd.Index(['Model', 'Round', 'Date', 'NewColumn1', 'NewColumn2'])
        ensure_summary_table(mock_conn, 'test_summary', columns)

        # Check that ALTER TABLE was called for new columns
        alter_table_calls = [call for call in mock_cursor.execute.call_args_list if 'ALTER TABLE' in str(call)]
        self.assertEqual(len(alter_table_calls), 2)

if __name__ == '__main__':
    unittest.main()