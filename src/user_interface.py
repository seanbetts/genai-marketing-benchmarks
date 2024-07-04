import curses
import os

def clear_console():
    """Clear the console screen."""
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')

def curses_menu(stdscr, items, prompt, all_selected=True):
    """
    Display a curses-based menu for selection.
    
    Args:
    stdscr: Standard screen object from curses
    items (list): List of items to select from
    prompt (str): Prompt to display at the top of the menu
    all_selected (bool): Whether all items should be selected by default
    
    Returns:
    list: Selected items
    """
    curses.curs_set(0)
    stdscr.clear()
    selected_rows = set(range(len(items))) if all_selected else set()
    current_row = 0

    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, prompt)
        stdscr.addstr(1, 0, "Use arrow keys to navigate, Space to toggle selection, Enter to confirm")
        for idx, item in enumerate(items):
            x = 0
            y = idx + 2  # Offset by 2 to account for the prompt and instruction lines
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, f"{'[X]' if idx in selected_rows else '[ ]'} {item}")
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, f"{'[X]' if idx in selected_rows else '[ ]'} {item}")
        
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(items) - 1:
            current_row += 1
        elif key == ord(' '):
            if current_row in selected_rows:
                selected_rows.remove(current_row)
            else:
                selected_rows.add(current_row)
        elif key in [10, 13]:  # Enter key
            break
        
        stdscr.refresh()

    return [items[idx] for idx in selected_rows]

def select_models(models):
    """
    Display a menu for model selection.
    
    Args:
    models (list): List of model dictionaries
    
    Returns:
    list: Selected models
    """
    items = [f"{model['name']} (Provider: {model['provider']})" for model in models]
    selected = curses.wrapper(curses_menu, items, "Select models (press Space to toggle, Enter to confirm):", all_selected=False)
    return [model for model in models if f"{model['name']} (Provider: {model['provider']})" in selected]

def select_categories(categories):
    """
    Display a menu for category selection.
    
    Args:
    categories (list): List of categories
    
    Returns:
    list: Selected categories
    """
    return curses.wrapper(curses_menu, categories, "Select categories (press Space to toggle, Enter to confirm):", all_selected=True)

def get_user_inputs():
    """
    Get user inputs for number of questions and rounds.
    
    Returns:
    tuple: (num_questions, num_rounds)
    """
    clear_console()
    num_questions_input = input("Enter the number of questions to test (or type 'All' to use all questions): ")
    num_questions = 'all' if num_questions_input.lower() == 'all' else int(num_questions_input)
    num_rounds = int(input("Enter the number of rounds to run: "))
    return num_questions, num_rounds

def confirm_run(estimated_cost, model_costs, num_rounds, num_questions, total_questions):
    """
    Display estimated costs and ask for user confirmation.
    
    Args:
    estimated_cost (float): Total estimated cost
    model_costs (list): List of tuples containing model names and their costs
    num_rounds (int): Number of rounds to run
    num_questions (int or str): Number of questions per round ('all' or int)
    total_questions (int): Total number of questions available
    
    Returns:
    bool: True if user confirms, False otherwise
    """
    clear_console()
    questions_per_round = total_questions if num_questions == 'all' else min(num_questions, total_questions)
    total_questions_run = questions_per_round * num_rounds
    
    print(f"\nEstimated cost for running {num_rounds} rounds with {questions_per_round} questions each across selected models:")
    for model_name, cost in model_costs:
        print(f"  {model_name}: ${cost:.3f}")
    print(f"Total estimated cost: ${estimated_cost:.3f}")
    
    confirm = input("\nDo you want to proceed with the testing run? (y/n): ").strip().lower()
    return confirm == 'y'