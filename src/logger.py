import logging
import os
from datetime import datetime

def setup_logger(base_folder):
    # Get current date and time
    today_date = datetime.today().strftime('%Y-%m-%d')
    current_time = datetime.now().strftime('%H-%M')

    # Set up folder
    logs_folder = os.path.join(base_folder, 'Logs')
    today_logs_folder = os.path.join(logs_folder, today_date)
    if not os.path.exists(today_logs_folder):
        os.makedirs(today_logs_folder)

    # Create log file
    log_file = os.path.join(today_logs_folder, f"run_{current_time}.log")

    # Create and configure logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create handlers
    file_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler()

    # Create formatters and add it to handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger