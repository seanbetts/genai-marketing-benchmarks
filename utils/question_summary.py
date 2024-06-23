import os
import sqlite3
from datetime import datetime
import curses
import pandas as pd
import re
from typing import List, Tuple, Optional
from functions import determine_provider, clean_model_name, clear_console

class DatabaseError(Exception):
    """Custom exception for database-related errors."""
    pass

def get_base_folder() -> str:
    """Get the base folder path."""
    try:
        current_file_path = os.path.abspath(__file__)
        return os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
    except Exception as e:
        raise OSError(f"Failed to determine base folder: {e}")

def get_table_names_with_timestamp(cursor: sqlite3.Cursor) -> List[str]:
    """Get table names that have a 'Timestamp' column."""
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        return [
            table for table in tables
            if any(column[1].lower() == 'timestamp' for column in cursor.execute(f"PRAGMA table_info('{table}');"))
        ]
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to retrieve table names: {e}")

def get_earliest_timestamp(cursor: sqlite3.Cursor, table_name: str) -> Optional[str]:
    """Get the earliest timestamp from a table."""
    try:
        cursor.execute(f"SELECT MIN(Timestamp) FROM '{table_name}';")
        return cursor.fetchone()[0]
    except sqlite3.Error as e:
        print(f"Warning: Failed to get earliest timestamp for table '{table_name}': {e}")
        return None

def create_summary_table(cursor: sqlite3.Cursor, conn: sqlite3.Connection) -> None:
    """Create a summary table."""
    try:
        cursor.execute("DROP TABLE IF EXISTS table_summary;")
        cursor.execute("""
            CREATE TABLE table_summary (
                table_name TEXT PRIMARY KEY,
                creation_date TEXT
            );
        """)
        conn.commit()
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to create summary table: {e}")

def populate_summary_table(cursor: sqlite3.Cursor, conn: sqlite3.Connection, table_names: List[str]) -> None:
    """Populate the summary table with table names and creation dates."""
    try:
        for table_name in table_names:
            earliest_timestamp = get_earliest_timestamp(cursor, table_name)
            if earliest_timestamp:
                formatted_date = datetime.strptime(earliest_timestamp, "%Y-%m-%d %H:%M:%S.%f").strftime("%d-%m-%Y")
                cursor.execute("INSERT INTO table_summary (table_name, creation_date) VALUES (?, ?);", 
                               (table_name, formatted_date))
        conn.commit()
    except sqlite3.Error as e:
        raise DatabaseError(f"Failed to populate summary table: {e}")
    except ValueError as e:
        raise ValueError(f"Failed to parse timestamp: {e}")

def curses_menu(stdscr, table_names: List[str]) -> List[str]:
    """Display a curses-based menu for table selection."""
    try:
        curses.curs_set(0)
        selected_tables = set()
        current_selection = 0
        table_names.append("Exit")

        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Select models (press Space to toggle, Enter to confirm):")
            for idx, table_name in enumerate(table_names):
                prefix = "[x]" if table_name in selected_tables else "[ ]"
                style = curses.A_REVERSE if idx == current_selection else curses.A_NORMAL
                stdscr.addstr(idx + 1, 0, f"{prefix} {table_name}", style)
            
            key = stdscr.getch()
            if key == curses.KEY_UP:
                current_selection = max(0, current_selection - 1)
            elif key == curses.KEY_DOWN:
                current_selection = min(len(table_names) - 1, current_selection + 1)
            elif key == ord(' '):
                table_name = table_names[current_selection]
                if table_name in selected_tables:
                    selected_tables.remove(table_name)
                else:
                    selected_tables.add(table_name)
            elif key in [10, 13]:  # Enter key
                if table_names[current_selection] == "Exit":
                    return []
                break

        return list(selected_tables)
    except curses.error as e:
        raise RuntimeError(f"Curses error: {e}")

def clean_table_name(name: str) -> str:
    """Clean the table name."""
    name = re.sub(r'^[0-9]+_[0-9]+_[0-9]+_', '', name)
    name = name.replace('_', '-')
    provider = determine_provider(name)
    return clean_model_name(name, provider)

def process_selected_tables(selected_tables: List[str], conn: sqlite3.Connection) -> pd.DataFrame:
    """Process selected tables and return a DataFrame."""
    try:
        df = pd.DataFrame()
        for table in selected_tables:
            query = f"SELECT Question_Code, Question, Category, Sub_Category, Correct FROM '{table}'"
            data = pd.read_sql_query(query, conn)
            data['Correct'] = data['Correct'].astype(bool)
            cleaned_table_name = clean_table_name(table)
            if df.empty:
                df = data[['Category', 'Sub_Category', 'Question_Code', 'Question']]
            df[cleaned_table_name] = data['Correct']
        return df
    except (sqlite3.Error, pd.errors.DatabaseError) as e:
        raise DatabaseError(f"Failed to process selected tables: {e}")

def main() -> None:
    try:
        clear_console()
        base_folder = get_base_folder()
        db_path = os.path.join(base_folder, 'results_database.sqlite')
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            table_names = get_table_names_with_timestamp(cursor)
            selected_tables = curses.wrapper(lambda stdscr: curses_menu(stdscr, table_names))
        
        if selected_tables:
            with sqlite3.connect(db_path) as conn:
                df = process_selected_tables(selected_tables, conn)
            
            today_date = datetime.today().strftime('%d-%m-%Y')
            output_path = os.path.join(base_folder, f'question_summary - {today_date}.csv')
            df.to_csv(output_path, index=False)
            print(f"DataFrame saved to {output_path}")
        else:
            print("No tables selected. Exiting.")
    except DatabaseError as e:
        print(f"Database error: {e}")
    except OSError as e:
        print(f"OS error: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
    except RuntimeError as e:
        print(f"Runtime error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()