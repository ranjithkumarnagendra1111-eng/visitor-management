# Visitor Management System

## Overview
This project implements a Visitor Management System with a focus on Python foundations, advanced OOP concepts, concurrency, and SQL database integration with REST API development. It includes modular code for handling employee and visitor data, API endpoints, proper logging/error handling, and database operations.

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

## Week 2: Advanced Python & OOP + Concurrency
This implementation covers:
- Object-Oriented Programming (OOP) concepts
- Singleton pattern for configuration management
- Interface-based design with abstract base classes
- Concurrency with threading and multiprocessing
- Parallel file processing
- Design patterns and architectural principles

### Key Features
- Singleton ConfigManager for centralized configuration
- Abstract base classes for DataLoader, Transformer, Writer
- VisitorManagementPipeline for data processing
- ConcurrencyExplorer for comparing threading vs multiprocessing
- CRUD operations for visitors, employees, and visits (JSON-based)

## Week 3: SQL + API Development
This implementation covers:
- SQL fundamentals: joins, aggregations, window functions, query optimization
- REST API development with FastAPI
- CRUD operations with database integration
- Input validation using Pydantic
- Error handling middleware
- Token-based authentication
- API versioning (/v1/)
- OpenAPI documentation

### Key Features
- SQLite database with tables for employees, visitors, visits
- SQL scripts for data ingestion, queries with joins/aggregations/window functions
- RESTful API endpoints: POST (load), GET (fetch), PUT (update), DELETE (remove)
- Request validation and standard response format
- HTTP status codes and error handling
- Authentication with Bearer tokens
- API versioning and auto-generated OpenAPI docs

## Project Structure
```
visitor-management/
├── src/
│   ├── main.py          # FastAPI app entry point
│   ├── config.py        # Configuration settings
│   ├── routes.py        # Main API routes
│   ├── models.py        # Data models
│   ├── data_manager.py  # Data management utilities
│   ├── week1/           # Week 1 specific implementation
│   │   ├── utils.py     # DataManager class for file operations
│   │   ├── routes.py    # Week 1 API routes
│   │   └── README.md    # Week 1 specific notes
│   ├── week2/           # Week 2 OOP and concurrency
│   │   ├── utils.py     # OOP classes and concurrency
│   │   ├── routes.py    # Week 2 API routes
│   │   ├── data_manager.py # JSON-based CRUD
│   │   ├── interfaces.py # Abstract base classes
│   │   └── models.py    # Pydantic models
│   └── week3/           # Week 3 SQL and API
│       ├── database.py  # SQLite database manager
│       ├── utils.py     # Data service layer
│       ├── routes.py    # Week 3 API routes
│       └── models.py    # Pydantic models for API
├── scripts/             # SQL scripts
│   ├── data_ingestion.sql # Data loading queries
│   └── queries.sql      # SQL queries examples
├── tests/               # Unit tests
│   ├── test_week1.py    # Week 1 tests
│   ├── test_week2.py    # Week 2 tests
│   └── test_week3.py    # Week 3 tests
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

## API Documentation (Week 3)

### Authentication
All Week 3 endpoints require authentication. First, obtain a token:

**POST /v1/login**
```json
{
  "username": "admin",
  "password": "password"
}
```

Use the returned `access_token` in the Authorization header:
```
Authorization: Bearer <access_token>
```

### Endpoints

#### Employees
- **GET /v1/employees** - Get all employees
- **GET /v1/employees/{id}** - Get employee by ID
- **PUT /v1/employees/{id}** - Update employee
- **DELETE /v1/employees/{id}** - Delete employee

#### Visitors
- **GET /v1/visitors** - Get all visitors
- **GET /v1/visitors/{id}** - Get visitor by ID
- **PUT /v1/visitors/{id}** - Update visitor
- **DELETE /v1/visitors/{id}** - Delete visitor

#### Visits
- **GET /v1/visits** - Get all visits
- **GET /v1/visits/{id}** - Get visit by ID
- **PUT /v1/visits/{id}** - Update visit
- **DELETE /v1/visits/{id}** - Delete visit

#### Data Loading
- **POST /v1/load-data** - Load data into tables
  ```json
  {
    "table": "employees|visitors|visits",
    "data": [...]
  }
  ```

#### Reports
- **GET /v1/reports/visits** - Get visit report with joins

## Testing

Run all tests:
```
python unittest.bat
```

Run specific test file:
```
pytest tests/test_week3.py -v --cov=src --cov-report term-missing
```

## SQL Scripts

Execute SQL scripts using SQLite:
```
sqlite3 data/visitor_management.db < scripts/data_ingestion.sql
sqlite3 data/visitor_management.db < scripts/queries.sql
```

## Postman Testing

1. Import the OpenAPI spec from http://localhost:8000/openapi.json
2. Set up authentication with Bearer token
3. Test CRUD operations on employees, visitors, and visits

## Requirements
- Python 3.8+
- Dependencies listed in `requirements.txt`

## Code Quality
- No hardcoding: All paths and settings are config-driven.
- Proper error handling: Exceptions are logged and raised appropriately.
- Reusable functions: Code is modular with classes and functions.
- Clean structure: Organized folders and modules.