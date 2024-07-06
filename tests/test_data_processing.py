import unittest
import pandas as pd
import os
import sqlite3
from unittest.mock import patch, MagicMock

from src.data_processing import (
    answer_check,
    calculate_token_cost,
    estimate_cost,
    sanitize_column_name,
    load_questions,
    save_results_to_sqlite,
    check_table_exists_and_get_highest_round,
    ensure_summary_table,
    get_sqlite_type
)
from src.constants import DATABASE_PATH

class TestDataProcessing(unittest.TestCase):

    def setUp(self):
        # Create a temporary database for testing
        self.test_db_path = 'test_database.sqlite'
        self.conn = sqlite3.connect(self.test_db_path)
        self.cursor = self.conn.cursor()

    def tearDown(self):
        # Close the connection and remove the temporary database
        self.conn.close()
        os.remove(self.test_db_path)

    # ... (keep existing test methods)

    @patch('src.data_processing.sqlite3.connect')
    def test_save_results_to_sqlite_new_table(self, mock_connect):
        test_data = {
            'Round': [1, 1],
            'Discipline': ['Math', 'Science'],
            'Category': ['Algebra', 'Physics'],
            'Question': ['Q1', 'Q2'],
            'Is_Correct': [True, False]
        }
        test_df = pd.DataFrame(test_data)

        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = None  # Table doesn't exist

        save_results_to_sqlite(test_df, 'TestModel', '2024-07-06', db_path=self.test_db_path)

        # Check if CREATE TABLE was called
        create_table_calls = [call for call in mock_cursor.execute.call_args_list if 'CREATE TABLE' in str(call)]
        self.assertTrue(len(create_table_calls) > 0)

        # Check if data was inserted
        mock_conn.commit.assert_called()

    @patch('src.data_processing.sqlite3.connect')
    def test_save_results_to_sqlite_existing_table(self, mock_connect):
        test_data = {
            'Round': [1, 1],
            'Discipline': ['Math', 'Science'],
            'Category': ['Algebra', 'Physics'],
            'Question': ['Q1', 'Q2'],
            'Is_Correct': [True, False]
        }
        test_df = pd.DataFrame(test_data)

        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = ('existing_table',)  # Table exists

        save_results_to_sqlite(test_df, 'TestModel', '2024-07-06', db_path=self.test_db_path)

        # Check if ALTER TABLE was called for new columns
        alter_table_calls = [call for call in mock_cursor.execute.call_args_list if 'ALTER TABLE' in str(call)]
        self.assertTrue(len(alter_table_calls) > 0)

        # Check if data was inserted
        mock_conn.commit.assert_called()

    def test_ensure_summary_table(self):
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        # Mocking the result of PRAGMA table_info(table_name)
        mock_cursor.fetchall.return_value = [
            (0, 'Model', 'TEXT', 0, None, 0),
            (1, 'Round', 'INTEGER', 0, None, 0),
            (2, 'Date', 'TEXT', 0, None, 0)
        ]
        
        columns = pd.Index(['NewColumn1', 'NewColumn2'])
        
        ensure_summary_table(mock_conn, 'test_summary', columns)
        
        # Check if CREATE TABLE IF NOT EXISTS was called
        mock_cursor.execute.assert_any_call("CREATE TABLE IF NOT EXISTS test_summary (Model TEXT, Round INTEGER, Date TEXT)")
        
        # Check if ALTER TABLE was called for new columns
        alter_table_calls = [call for call in mock_cursor.execute.call_args_list if 'ALTER TABLE' in str(call)]
        self.assertEqual(len(alter_table_calls), 2)  # Two new columns should be added
        
        # Check the specific ALTER TABLE calls
        mock_cursor.execute.assert_any_call("ALTER TABLE test_summary ADD COLUMN NewColumn1 REAL")
        mock_cursor.execute.assert_any_call("ALTER TABLE test_summary ADD COLUMN NewColumn2 REAL")

    def test_get_sqlite_type(self):
        self.assertEqual(get_sqlite_type('int64'), 'INTEGER')
        self.assertEqual(get_sqlite_type('float64'), 'REAL')
        self.assertEqual(get_sqlite_type('object'), 'TEXT')
        self.assertEqual(get_sqlite_type(pd.Series([True, False]).dtype), 'TEXT')

if __name__ == '__main__':
    unittest.main()