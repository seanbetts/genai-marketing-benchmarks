import unittest
import pandas as pd
import os
import sqlite3

from src.data_processing import (
    answer_check,
    calculate_token_cost,
    estimate_cost,
    sanitize_column_name,
    load_questions,
    save_results_to_sqlite,
    check_table_exists_and_get_highest_round
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

    def test_answer_check(self):
        self.assertEqual(answer_check("A"), ("A", True))
        self.assertEqual(answer_check("E"), ("E", False))
        self.assertEqual(answer_check("a"), ("A", True))
        self.assertEqual(answer_check(" B "), ("B", True))
        self.assertEqual(answer_check("**C**"), ("C", True))
        self.assertEqual(answer_check("#D#"), ("D", True))
        self.assertEqual(answer_check(""), ("", False))
        self.assertEqual(answer_check("AB"), ("A", True))

    def test_calculate_token_cost(self):
        model_info = {"prompt": 0.001, "completion": 0.002}
        self.assertAlmostEqual(calculate_token_cost(10, 5, model_info), 0.02)
        self.assertAlmostEqual(calculate_token_cost(0, 0, model_info), 0)
        self.assertAlmostEqual(calculate_token_cost(100, 50, model_info), 0.2)

    def test_estimate_cost(self):
        models = [
            {"name": "Model1", "prompt": 0.001, "completion": 0.002},
            {"name": "Model2", "prompt": 0.002, "completion": 0.003}
        ]
        num_questions = 100
        num_rounds = 2
        avg_prompt_tokens = 70
        avg_completion_tokens = 1
        
        total_cost, model_costs = estimate_cost(num_questions, num_rounds, models, avg_prompt_tokens, avg_completion_tokens)
        
        expected_cost_model1 = 200 * ((0.001 * 70) + (0.002 * 1))  # 14.4
        expected_cost_model2 = 200 * ((0.002 * 70) + (0.003 * 1))  # 28.6
        expected_total_cost = expected_cost_model1 + expected_cost_model2  # 43.0
        
        self.assertAlmostEqual(total_cost, expected_total_cost, places=2)
        self.assertEqual(len(model_costs), 2)
        self.assertAlmostEqual(model_costs[0][1], expected_cost_model1, places=2)
        self.assertAlmostEqual(model_costs[1][1], expected_cost_model2, places=2)

    def test_sanitize_column_name(self):
        self.assertEqual(sanitize_column_name("Normal Name"), "Normal_Name")
        self.assertEqual(sanitize_column_name("With-Hyphen"), "With_Hyphen")
        self.assertEqual(sanitize_column_name("With.Dot"), "With_Dot")
        self.assertEqual(sanitize_column_name("With Space"), "With_Space")
        self.assertEqual(sanitize_column_name("123Number"), "123Number")
        self.assertEqual(sanitize_column_name("Special@#$"), "Special___")

    def test_load_questions(self):
        # Create a test table
        self.cursor.execute('''CREATE TABLE questions
                             (id INTEGER PRIMARY KEY, Question TEXT, Category TEXT)''')
        self.cursor.executemany('INSERT INTO questions (Question, Category) VALUES (?, ?)',
                                [('Test Question 1', 'Category A'),
                                 ('Test Question 2', 'Category B')])
        self.conn.commit()

        # Test loading questions
        questions_df = load_questions(db_path=self.test_db_path)
        self.assertIsInstance(questions_df, pd.DataFrame)
        self.assertEqual(len(questions_df), 2)
        self.assertIn('Question', questions_df.columns)
        self.assertIn('Category', questions_df.columns)

    def test_save_results_to_sqlite(self):
        # Create a test DataFrame
        test_data = {
            'Round': [1, 1],
            'Question': ['Q1', 'Q2'],
            'Is_Correct': [True, False]
        }
        test_df = pd.DataFrame(test_data)

        # Save results
        save_results_to_sqlite(test_df, 'TestModel', '2024-07-06', db_path=self.test_db_path)

        # Verify results were saved
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='2024_07_06_TestModel'")
        self.assertIsNotNone(self.cursor.fetchone())

    def test_check_table_exists_and_get_highest_round(self):
        # Create a test table
        self.cursor.execute('''CREATE TABLE "2024_07_06_TestModel"
                             (id INTEGER PRIMARY KEY, Round INTEGER)''')
        self.cursor.executemany('INSERT INTO "2024_07_06_TestModel" (Round) VALUES (?)',
                                [(1,), (2,), (3,)])
        self.conn.commit()

        # Test function
        highest_round = check_table_exists_and_get_highest_round('TestModel', '2024-07-06', db_path=self.test_db_path)
        self.assertEqual(highest_round, 3)

        # Test with non-existent table
        highest_round = check_table_exists_and_get_highest_round('NonExistentModel', '2024-07-06', db_path=self.test_db_path)
        self.assertEqual(highest_round, 0)

if __name__ == '__main__':
    unittest.main()