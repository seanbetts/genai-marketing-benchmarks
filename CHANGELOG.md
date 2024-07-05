# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - dev branch

### Added
- Implemented type hints across all main Python files for improved code readability and error catching.
- Added docstrings to all functions following Google style format.
- Created a `config.yaml` file to store model information and other settings.
- Implemented list comprehensions in various parts of the code for improved efficiency.
- Implemented a Command Line Interface (CLI) using the `click` library, allowing for both interactive and non-interactive modes of operation.
- Added CLI options for specifying number of questions, number of rounds, models to use, and categories to test.
- Implemented environment variable checks to ensure necessary API keys are set before running the benchmark.

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

### Removed
- Removed the original `test.py` file after migrating all functionality to new modular structure.

### Improved
- Enhanced the project's flexibility by allowing users to run the benchmark with specific parameters without modifying the code.
- Streamlined the process of running the benchmark through command-line arguments.

## [0.1.0-beta] - 2024-06-24 - main branch (current release)

### Added
- Initial project setup.
- Basic functionality for querying language models and processing results.
- SQLite database integration for storing test results.
- Simple command-line interface for user interactions.
- Created a comprehensive README.md file explaining the project's purpose, challenges, and current status.

[Unreleased]: https://github.com/seanbetts/genai-marketing-benchmarks/tree/dev
[0.1.0-beta]: https://github.com/seanbetts/genai-marketing-benchmarks/tree/0.1.0-beta