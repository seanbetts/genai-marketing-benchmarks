import os
import sys

def add_project_root_to_path():
    # Get the directory containing the current script (utils)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get the parent directory of utils (which should be the project root)
    project_root = os.path.dirname(current_dir)
    
    # Add the project root to sys.path if it's not already there
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

# Call this function at the top of your markdown.py file
add_project_root_to_path()

import sqlite3
import pandas as pd
from datetime import datetime
import curses
from utils.utils import determine_provider, clean_model_name, clear_console
from src.constants import DATABASE_PATH

# Clear console
clear_console()

# Verify database
def verify_database_path(path):
       if not os.path.exists(path):
           raise FileNotFoundError(f"Database file not found: {path}")
       # print(f"Database file found: {path}")

# Function to initialize the database connection and fetch dates
def get_models():
    verify_database_path(DATABASE_PATH)
    conn = sqlite3.connect(DATABASE_PATH)
    query = "SELECT Model, Date, TOTAL as Score FROM category_summary ORDER BY Date DESC, TOTAL DESC"
    models_df = pd.read_sql_query(query, conn)
    conn.close()

    # Apply determine_provider and clean_model_name functions
    models_df['Provider'] = models_df['Model'].apply(determine_provider)
    models_df['CleanModel'] = models_df.apply(lambda row: clean_model_name(row['Model'], row['Provider']), axis=1)

    return models_df

# Function to select models using curses menu
def curses_model_menu(models_df):
    stdscr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)
    
    models = models_df.to_dict('records')
    selected_models = set()
    idx = 0
    
    try:
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Use arrow keys to navigate, Space to select/deselect, and Enter to confirm all selections.")
            stdscr.addstr(1, 0, "Press Ctrl+C to exit at any time.\n")
            for i, model in enumerate(models):
                display_text = f"{model['Date']} - {model['CleanModel']} - Score: {model['Score']:.1f}%"
                if i == idx:
                    stdscr.addstr(i + 3, 0, f"{'[X]' if model['Model'] in selected_models else '[ ]'} {display_text}", curses.A_REVERSE)
                else:
                    stdscr.addstr(i + 3, 0, f"{'[X]' if model['Model'] in selected_models else '[ ]'} {display_text}")
            stdscr.refresh()
            
            key = stdscr.getch()
            
            if key == curses.KEY_UP and idx > 0:
                idx -= 1
            elif key == curses.KEY_DOWN and idx < len(models) - 1:
                idx += 1
            elif key == ord(' '):
                model = models[idx]['Model']
                if model in selected_models:
                    selected_models.remove(model)
                else:
                    selected_models.add(model)
            elif key in [curses.KEY_ENTER, 10, 13]:  # Enter key
                if len(selected_models) > 0:
                    return list(selected_models)
                else:
                    stdscr.addstr(len(models) + 3, 0, "Please select at least one model before confirming.", curses.A_BOLD)
                    stdscr.refresh()
                    stdscr.getch()  # Wait for any key press
    except KeyboardInterrupt:
        return None
    finally:
        curses.endwin()

# Main function to generate markdown file
def generate_markdown(selected_models):
    # Connect to SQLite database
    verify_database_path(DATABASE_PATH)
    conn = sqlite3.connect(DATABASE_PATH)

    # Read data from category_summary table with selected models
    placeholders = ', '.join(['?' for _ in selected_models])
    query = f"SELECT * FROM category_summary WHERE Model IN ({placeholders})"
    df = pd.read_sql_query(query, conn, params=selected_models)

    # Close the connection
    conn.close()

    # Apply determine_provider and clean_model_name functions
    df['Provider'] = df['Model'].apply(determine_provider)
    df['CleanModel'] = df.apply(lambda row: clean_model_name(row['Model'], row['Provider']), axis=1)

    # Rename columns as needed
    column_renames = {
        'TOTAL': 'TOTAL↓',
        'Ad_Ops': 'Ad Ops',
        'Comms_Planning': 'Comms Planning',
        'Marketing_Effectiveness': 'Marketing Effectiveness',
        'Paid_Search': 'Paid Search',
        'Paid_Social': 'Paid Social',
        'Privacy___Ethics': 'Privacy & Ethics',
        'Web_Analytics': 'Web Analytics',
        'Content_Marketing': 'Content Marketing',
        'Influencer_Marketing': 'Influencer Marketing',
        'Market_Research___Insights': 'Market Research & Insights',
    }

    df.rename(columns=column_renames, inplace=True)

    # Add Provider column based on Model
    df['Provider'] = df['Model'].apply(determine_provider)

    # Clean up Model names for each provider
    df['Model'] = df.apply(lambda row: clean_model_name(row['Model'], row['Provider']), axis=1)

    # Convert relevant columns to numeric and round to one decimal place
    numeric_columns = df.columns.difference(['Provider', 'Model'])
    df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce').round(1)

    # Sort the DataFrame by 'TOTAL↓' in descending order
    df.sort_values(by='TOTAL↓', ascending=False, inplace=True)

    # Find the maximum value in each numeric column
    max_values = df[numeric_columns].max()

    # Add percentage sign to numeric columns and bold the maximum values
    for col in numeric_columns:
        df[col] = df[col].apply(lambda x: f"**{x}%**" if x == max_values[col] else f"{x}%")

    # Define the structure of the markdown table
    headers = ["Provider", "Model", "TOTAL↓", "AV", "Ad Ops", "Affiliates", "Audio", "Cinema", 
               "Comms Planning", "Marketing Effectiveness", "Outdoor", "Paid Search", "Paid Social", 
               "Privacy & Ethics", "Programmatic", "Publishing", "SEO", "Web Analytics", "eCommerce", "Content Marketing", "Influencer Marketing", "Market Research & Insights"]

    # Create the markdown table
    markdown_table = "| " + " | ".join(headers) + " |\n"
    markdown_table += "| " + " | ".join(["-"*len(header) for header in headers]) + " |\n"

    for index, row in df.iterrows():
        markdown_table += "| " + " | ".join(str(row.get(header, "")) for header in headers) + " |\n"

    # Get today's date
    today_date = datetime.today().strftime('%d-%m-%Y')

    # Write the markdown table to a file with today's date in the filename
    file_name = f"../Results/Marketing Benchmark Results - {today_date}.md"
    with open(file_name, "w") as file:
        file.write(markdown_table)

    print("Markdown file created successfully")

# Main script execution
def main():
    try:
        models_df = get_models()
        selected_models = curses_model_menu(models_df)
        
        # Cleanup curses
        curses.endwin()
        
        if selected_models:
            generate_markdown(selected_models)
        else:
            print("\nNo models selected or operation cancelled. Exiting...")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user. Exiting...")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    main()
