import sqlite3
import pandas as pd
from datetime import datetime
import curses
from utils import determine_provider, clean_model_name, clear_console

# Clear console
clear_console()

# Function to initialize the database connection and fetch dates
def get_dates():
    conn = sqlite3.connect('../../results_database.sqlite')
    query = "SELECT Date, COUNT(*) as record_count, AVG(TOTAL) as total_avg FROM category_summary GROUP BY Date"
    dates_df = pd.read_sql_query(query, conn)
    conn.close()
    return dates_df

# Function to select a date using curses menu
def curses_menu(dates_df):
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(True)
    
    dates = dates_df['Date'].tolist()
    selected_date = None
    idx = 0
    
    try:
        while True:
            stdscr.clear()
            stdscr.addstr(0, 0, "Use the arrow keys to navigate and press Enter to select a date.")
            stdscr.addstr(1, 0, "The markdown table will include data from the selected date onwards.\n")
            for i, date in enumerate(dates):
                record_count = dates_df.loc[dates_df['Date'] == date, 'record_count'].values[0]
                total_avg = dates_df.loc[dates_df['Date'] == date, 'total_avg'].values[0]
                display_text = f"{date} - {record_count} models included, AVERAGE SCORE: {total_avg:.1f}%"
                if i == idx:
                    stdscr.addstr(i + 3, 0, f"(X) {display_text}", curses.A_REVERSE)
                else:
                    stdscr.addstr(i + 3, 0, f"( ) {display_text}")
            stdscr.addstr(len(dates) + 3, 0, "( ) Exit")
            if idx == len(dates):
                stdscr.addstr(len(dates) + 3, 0, "(X) Exit", curses.A_REVERSE)
            stdscr.refresh()
            
            key = stdscr.getch()
            
            if key == curses.KEY_UP and idx > 0:
                idx -= 1
            elif key == curses.KEY_DOWN and idx < len(dates):
                idx += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if idx == len(dates):
                    selected_date = None
                else:
                    selected_date = dates[idx]
                break
    finally:
        curses.endwin()
    
    return selected_date

# Main function to generate markdown file
def generate_markdown(selected_date):
    # Connect to SQLite database
    conn = sqlite3.connect('../../results_database.sqlite')

    # Read data from category_summary table with selected date
    df = pd.read_sql_query(f"SELECT * FROM category_summary WHERE Date >= '{selected_date}'", conn)

    # Close the connection
    conn.close()

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
if __name__ == "__main__":
    dates = get_dates()
    selected_date = curses_menu(dates)
    if selected_date:
        generate_markdown(selected_date)
    else:
        print("No date selected. Exiting...")
