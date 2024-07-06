# Generate Provider based on Model
import re
import os
import platform

# Clear console
def clear_console():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

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