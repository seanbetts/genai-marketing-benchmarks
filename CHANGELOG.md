# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - dev branch


## [0.2.0-beta] - 2024-07-06 - main branch (current release)

### Added
- Implemented type hints across all main Python files for improved code readability and error catching.
- Added docstrings to all functions following Google style format.
- Created a `config.yaml` file to store model information and other settings.
- Implemented list comprehensions in various parts of the code for improved efficiency.
- Implemented a Command Line Interface (CLI) using the `click` library, allowing for both interactive and non-interactive modes of operation.
- Added CLI options for specifying number of questions, number of rounds, models to use, and categories to test.
- Implemented environment variable checks to ensure necessary API keys are set before running the benchmark.
- Created a `requirements.txt` file to specify project dependencies.
- Added an "Installing The GenAI Marketing Benchmarks" section to the README.
- Added a "Running The GenAI Marketing Benchmarks" section to the README.
- Implemented comprehensive unit tests for data processing functions.
- Created a `tests` directory with `test_api_calls.py`, `test_cli.py`, `test_constants.py`, `test_data_processing.py`, and `test_user_interface.py`.
- Added flexibility to database-related functions with optional `db_path` parameter.
- Implemented comprehensive type checking using mypy across the project.

### Changed
- Reorganized project structure:
  - Created a `src` directory for most Python modules.
  - Moved utility scripts to a `utils` directory within `src`.
  - Moved the main script functionality to `main.py` in the root directory.
- Modularized the code by breaking down `test.py` into smaller, purpose-specific files (`api_calls.py`, `data_processing.py`, `user_interface.py`).
- Improved naming conventions across the project for better code readability.
- Organized imports in all files, grouping them into standard library, third-party, and local imports.
- Enhanced error handling by wrapping API calls and file operations in try-except blocks.
- Implemented context managers for file operations and database connections.
- Moved sensitive information (API keys) to environment variables.
- Optimized database operations in `save_results_to_sqlite` by implementing batch inserts.
- Refactored `main.py` to use the new CLI structure.
- Improved error handling for missing environment variables.
- Updated the README structure to improve clarity and user guidance.
- Refined the `estimate_cost` function in `data_processing.py` to improve accuracy.
- Refined database handling in `data_processing.py` to improve testability and flexibility.
- Updated `load_questions`, `save_results_to_sqlite`, and `check_table_exists_and_get_highest_round` functions to accept custom database paths.

### Improved
- Enhanced the project's flexibility by allowing users to run the benchmark with specific parameters without modifying the code.
- Streamlined the process of running the benchmark through command-line arguments.
- Enhanced code reliability and maintainability through unit testing.
- Increased test coverage for critical api calls, CLI, data processing, and user interface functions.
- Improved type annotations across all modules to resolve mypy errors.
- Updated iteration logic in cli.py to use enumerate for question numbering, ensuring type safety with DataFrame indices.
- Refactored error handling in various functions to properly handle potential None values.
- Increased robustness of the codebase by eliminating potential type-related runtime errors.

### Removed
- Removed the original `test.py` file after migrating all functionality to new modular structure.

## [0.1.0-beta] - 2024-06-24 - main branch (current release)

### Added
- Initial project setup.
- Basic functionality for querying language models and processing results.
- SQLite database integration for storing test results.
- Simple command-line interface for user interactions.
- Created a comprehensive README.md file explaining the project's purpose, challenges, and current status.

[Unreleased]: https://github.com/seanbetts/genai-marketing-benchmarks/tree/dev
[0.1.0-beta]: https://github.com/seanbetts/genai-marketing-benchmarks/tree/0.1.0-beta