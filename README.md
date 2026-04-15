# Visitor Management System

## Overview
This project implements a Visitor Management System with a focus on Python foundations and code quality. It includes modular code for handling employee data, API endpoints, and proper logging/error handling.

## Week 1: Python Foundations & Code Quality
This implementation covers:
- Data types and mutability
- Functions and parameter passing
- Error handling
- Logging (replacing print statements)
- File handling (CSV/JSON read/write, temporary files)
- Project structure and modules
- Virtual environments and dependency management

### Key Features
- Modular structure with `src/` containing main modules
- Config-driven execution using `src/config.py`
- Logging enabled application
- API endpoints for data ingestion
- Proper exception handling throughout

## Project Structure
```
visitor-management/
├── src/
│   ├── main.py          # FastAPI app entry point
│   ├── config.py        # Configuration settings
│   ├── routes.py        # Main API routes
│   ├── models.py        # Data models
│   ├── data_manager.py  # Data management utilities
│   └── week1/           # Week 1 specific implementation
│       ├── utils.py     # DataManager class for file operations
│       ├── routes.py    # Week 1 API routes
│       └── README.md    # Week 1 specific notes
├── tests/               # Unit tests
├── data/                # Data files (CSV/JSON)
├── logs/                # Application logs
├── requirements.txt     # Python dependencies
├── README.md            # This file
└── venv/                # Virtual environment (not committed)
```

## Setup Instructions

1. **Clone or navigate to the project directory**:
   ```
   cd path/to/visitor-management
   ```

2. **Activate the virtual environment**:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```
   uvicorn src.main:app --reload
   ```

5. **Access the API**:
   - Root endpoint: `http://127.0.0.1:8000/`
   - Week 1 endpoint: `POST http://127.0.0.1:8000/week1/ingest_bulk_employees`

## Usage
- The Week 1 implementation ingests employee data from `data/employees.csv`, writes it to `data/employees.json`, and creates a temporary JSON file for demonstration.
- API response includes the number of ingested employees and the path to the temporary file.

## Testing
Run tests with:
```
pytest tests/
```

## Requirements
- Python 3.8+
- Dependencies listed in `requirements.txt`

## Code Quality
- No hardcoding: All paths and settings are config-driven.
- Proper error handling: Exceptions are logged and raised appropriately.
- Reusable functions: Code is modular with classes and functions.
- Clean structure: Organized folders and modules.