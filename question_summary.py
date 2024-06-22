import os
import sqlite3
from datetime import datetime
import curses
import pandas as pd
import re
from utils.functions import determine_provider, clean_model_name, clear_console

clear_console()

# Set up folder
base_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_table_names_with_timestamp(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    
    tables_with_timestamp = []
    for table in tables:
        cursor.execute(f"PRAGMA table_info('{table}');")  # Properly quote the table name
        columns = cursor.fetchall()
        for column in columns:
            if column[1].lower() == 'timestamp':  # Check for the Timestamp column
                tables_with_timestamp.append(table)
                break

    return tables_with_timestamp

def get_earliest_timestamp(cursor, table_name):
    cursor.execute(f"SELECT MIN(Timestamp) FROM '{table_name}';")  # Properly quote the table name
    return cursor.fetchone()[0]

def create_summary_table(cursor, conn):
    cursor.execute("DROP TABLE IF EXISTS table_summary;")
    cursor.execute("""
        CREATE TABLE table_summary (
            table_name TEXT PRIMARY KEY,
            creation_date TEXT  -- Change type to TEXT for date format
        );
    """)
    conn.commit()

def populate_summary_table(cursor, conn, table_names):
    for table_name in table_names:
        earliest_timestamp = get_earliest_timestamp(cursor, table_name)
        if earliest_timestamp:
            formatted_date = datetime.strptime(earliest_timestamp, "%Y-%m-%d %H:%M:%S.%f").strftime("%d-%m-%Y")
            cursor.execute("INSERT INTO table_summary (table_name, creation_date) VALUES (?, ?);", 
                           (table_name, formatted_date))
    conn.commit()

def curses_menu(stdscr, table_names):
    curses.curs_set(0)  # Hide cursor
    stdscr.clear()
    selected_tables = set()
    current_selection = 0

    # Add "Exit" option
    table_names.append("Exit")

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Select models (press Space to toggle, Enter to confirm):")
        for idx, table_name in enumerate(table_names):
            if idx == current_selection:
                if table_name in selected_tables:
                    stdscr.addstr(idx + 1, 0, f"[x] {table_name}", curses.A_REVERSE)
                else:
                    stdscr.addstr(idx + 1, 0, f"[ ] {table_name}", curses.A_REVERSE)
            else:
                if table_name in selected_tables:
                    stdscr.addstr(idx + 1, 0, f"[x] {table_name}")
                else:
                    stdscr.addstr(idx + 1, 0, f"[ ] {table_name}")
        key = stdscr.getch()

        if key == curses.KEY_UP and current_selection > 0:
            current_selection -= 1
        elif key == curses.KEY_DOWN and current_selection < len(table_names) - 1:
            current_selection += 1
        elif key == ord(' '):
            table_name = table_names[current_selection]
            if table_name in selected_tables:
                selected_tables.remove(table_name)
            else:
                selected_tables.add(table_name)
        elif key in [10, 13]:  # Handle Enter key
            if table_names[current_selection] == "Exit":
                return []
            break

    if table_names[current_selection] == "Exit":
        return []

    return list(selected_tables)

def clean_table_name(name):
    # Replace underscores with hyphens and remove all leading numbers and underscores
    name = re.sub(r'^[0-9]+_[0-9]+_[0-9]+_', '', name)
    name = name.replace('_', '-')
    # Get provider
    provider = determine_provider(name)
    name = clean_model_name(name, provider)
    return name

def main(stdscr):
    db_path = os.path.join(base_folder, 'results_database.sqlite')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    table_names = get_table_names_with_timestamp(cursor)
    selected_tables = curses_menu(stdscr, table_names)
    
    conn.close()
    return selected_tables

if __name__ == "__main__":
    selected_tables = curses.wrapper(main)
    if selected_tables:
        db_path = os.path.join(base_folder, 'results_database.sqlite')
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create a pandas DataFrame to store the results
        df = pd.DataFrame()
        
        for table in selected_tables:
            query = f"SELECT Question, Category, Sub_Category, Correct FROM '{table}'"
            data = pd.read_sql_query(query, conn)
            data['Correct'] = data['Correct'].map({1: True, 0: False})  # Replace 1 with True and 0 with False
            cleaned_table_name = clean_table_name(table)
            if 'Category' not in df.columns:
                df['Category'] = data['Category']
            if 'Sub_Category' not in df.columns:
                df['Sub_Category'] = data['Sub_Category']
            if 'Question' not in df.columns:
                df['Question'] = data['Question']
            df[cleaned_table_name] = data['Correct']
        
        # Get today's date
        today_date = datetime.today().strftime('%d-%m-%Y')
        
        # Save the DataFrame to a CSV file
        df.to_csv(os.path.join(base_folder, f'question_summary - {today_date}.csv'), index=False)
        print(f"DataFrame saved to question_summary - {today_date}.csv")
        
        conn.close()
