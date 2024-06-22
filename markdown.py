import sqlite3
import pandas as pd
import re
from datetime import datetime

# Connect to SQLite database
conn = sqlite3.connect('../results_database.sqlite')

# Read data from category_summary table
df = pd.read_sql_query("SELECT * FROM category_summary", conn)

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
}

df.rename(columns=column_renames, inplace=True)

# Generate Provider based on Model
def determine_provider(model_name):
    model_name_lower = model_name.lower()  # Convert to lower case for case insensitive comparison
    if 'claude' in model_name_lower:
        return 'Anthropic'
    elif 'gpt' in model_name_lower:
        return 'OpenAI'
    elif 'gemini' in model_name_lower:
        return 'Google'
    elif 'llama' in model_name_lower:
        return 'Meta'
    elif 'mistral' in model_name_lower:
        return 'Mistral'
    else:
        return 'Unknown'

df['Provider'] = df['Model'].apply(determine_provider)

# Clean up Model names for each provider
def clean_model_name(model_name, provider):
    if provider == 'Anthropic':
        # Remove date-like strings
        model_name = re.sub(r'\d{8}', '', model_name)
        # Replace hyphens with spaces
        model_name = model_name.replace('-', ' ')
        # Format numbers correctly
        model_name = re.sub(r'(\d) (\d)', r'\1.\2', model_name)
        # Capitalize and format with a space after the model number
        model_name_parts = model_name.split()
        model_name = f"{model_name_parts[0].title()}-{model_name_parts[1]} {model_name_parts[2].title()}"
    elif provider == 'OpenAI':
        # Remove date-like strings and trailing segments
        model_name = re.sub(r'\d{4}[-/]?\d{2}[-/]?\d{2}', '', model_name)
        model_name = re.sub(r'-\d+$', '', model_name)
        # Add hyphen after GPT, lowercase the "o", and remove trailing hyphens
        model_name = model_name.upper().replace(' ', '').replace('GPT', 'GPT-')
        model_name = re.sub(r'(\d)O', r'\1o', model_name)
        model_name = re.sub(r'-+', '-', model_name).rstrip('-')
        # Capitalize Turbo correctly and replace hyphen with space
        model_name = model_name.replace('TURBO', 'Turbo')
        model_name = model_name.replace('-Turbo', ' Turbo')
    elif provider == 'Google':
        # Remove date-like strings if any
        model_name = re.sub(r'\d{4}[-/]?\d{2}[-/]?\d{2}', '', model_name)
        # Add hyphen after Gemini
        model_name = model_name.replace('Gemini', 'Gemini-')
        # Capitalize first letter of each word and format correctly
        model_name = re.sub(r'(\b[a-z])', lambda x: x.group().upper(), model_name)
        # Remove last hyphen before type
        model_name = re.sub(r'-(Pro|Flash)$', r' \1', model_name)
    elif provider == 'Meta':
        # Remove everything before the forward slash
        model_name = model_name.split('/')[-1]
        # Remove date-like strings and trailing segments
        model_name = re.sub(r'\d{4}[-/]?\d{2}[-/]?\d{2}', '', model_name)
        # Add a hyphen after 'Llama'
        model_name = re.sub(r'(Llama) (\d)', r'\1-\2', model_name)
        # Remove everything after the 'B'
        model_name = re.sub(r'b.*', 'B', model_name)
        # Capitalize properly
        model_name = model_name.title()
        # Remove any extra hyphen or space after B
        model_name = re.sub(r'(\d)B', r'\1B', model_name)
        # Ensure there's no trailing hyphen or space
        model_name = model_name.strip('- ')
        model_name = model_name.replace('2-', '2 ')
        model_name = model_name.replace('3-', '3 ')
    elif provider == 'Mistral':
        # Remove everything before the forward slash
        model_name = model_name.split('/')[-1]
        # Remove "Instruct" and anything after
        model_name = re.sub(r'Instruct.*', '', model_name, flags=re.IGNORECASE)
        # Convert "X" to lowercase
        model_name = re.sub(r'X(\d)', r'x\1', model_name)
        # Remove trailing hyphen
        model_name = model_name.rstrip('-')
        # Capitalize properly
        model_name = re.sub(r'(\b[a-z])', lambda x: x.group().upper(), model_name)
    else:
        # Generic cleanup
        model_name = model_name.replace('-', ' ')
    return model_name

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
           "Privacy & Ethics", "Programmatic", "Publishing", "SEO", "Web Analytics", "eCommerce"]

# Create the markdown table
markdown_table = "| " + " | ".join(headers) + " |\n"
markdown_table += "| " + " | ".join(["-"*len(header) for header in headers]) + " |\n"

for index, row in df.iterrows():
    markdown_table += "| " + " | ".join(str(row.get(header, "")) for header in headers) + " |\n"

# Get today's date
today_date = datetime.today().strftime('%d-%m-%Y')

# Write the markdown table to a file with today's date in the filename
file_name = f"Results/Marketing Benchmark Results - {today_date}.md"
with open(file_name, "w") as file:
    file.write(markdown_table)

print("Markdown file created successfully")
