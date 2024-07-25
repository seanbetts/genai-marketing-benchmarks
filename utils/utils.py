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
    model_name_lower = model_name.lower()
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
import re

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
        # Capitalize Mini correctly and replace hyphen with space
        model_name = model_name.replace('MINI', 'Mini')
        model_name = model_name.replace('-Mini', ' Mini')
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
        # Try to match both Llama-3.1 and Llama-2 style names
        match = re.search(r'Llama[-\s]*(\d+(?:\.\d+)?)[-\s]*(\d+)[bB]', model_name, re.IGNORECASE)
        if match:
            version, size = match.groups()
            # Remove trailing .0 if present
            version = version.rstrip('.0')
            model_name = f"Llama-{version} {size}B"
        else:
            # If pattern not found, just clean up the name
            model_name = re.sub(r'Meta-?', '', model_name)
            model_name = re.sub(r'Instruct.*', '', model_name)
            model_name = re.sub(r'chat.*', '', model_name, flags=re.IGNORECASE)
            model_name = re.sub(r'[-\s]+', '-', model_name).strip('-')
        # Remove -hf suffix if present
        model_name = re.sub(r'-hf$', '', model_name, flags=re.IGNORECASE)
    elif provider == 'Mistral':
        # Remove everything before the forward slash
        model_name = model_name.split('/')[-1]
        # Remove "Instruct", "latest", and anything after
        model_name = re.sub(r'(Instruct|latest).*', '', model_name, flags=re.IGNORECASE)
        # Convert "X" to lowercase
        model_name = re.sub(r'X(\d)', r'x\1', model_name)
        # Remove hyphens and extra spaces
        model_name = re.sub(r'[-\s]+', ' ', model_name).strip()
        # Capitalize properly
        model_name = ' '.join(word.capitalize() for word in model_name.split())
    else:
        # Generic cleanup
        model_name = model_name.replace('-', ' ')
    
    return model_name