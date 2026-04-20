# Week 1: Python Foundations & Code Quality

This module key Python concepts through separate API endpoints.

## Endpoints

### 1. Data Types & Mutability
- **Endpoint**: `GET /week1/data-types-mutability`
- **Description**: Shows examples of immutable (str, int, tuple) and mutable (list, dict) data types, demonstrating mutability.

### 2. Functions & Parameter Passing
- **Endpoint**: `GET /week1/functions-parameter-passing/{name}/{age}`
- **Description**:  function calls with path parameters.
- **Example**: `/week1/functions-parameter-passing/John/25`

### 3. Error Handling
- **Endpoint**: `GET /week1/error-handling/{trigger_error}`
- **Description**: Shows proper exception handling. Set `trigger_error=true` to see error handling in action.
- **Example**: `/week1/error-handling/false` (success) or `/week1/error-handling/true` (error)

### 4. Logging vs Print
- **Endpoint**: `GET /week1/logging-demo`
- **Description**:  logging at different levels (debug, info, warning, error) instead of print statements.

### 5. File Handling
- **Endpoint**: `GET /week1/file-handling-demo`
- **Description**: Shows basic file read/write operations using temporary files.
- **Also see**: `POST /week1/ingest_bulk_employees` for CSV/JSON handling.

### 6. Project Structure & Modules
- **Endpoint**: `GET /week1/project-structure-modules`
- **Description**:  module imports and project structure usage.

### 7. Virtual Environments
- **Endpoint**: `GET /week1/virtual-environments`
- **Description**: Shows virtual environment detection and Python environment info.

## Original File Handling Demo
- **Endpoint**: `POST /week1/ingest_bulk_employees`
- **Description**: Reads data/employees.csv (20 records), writes to data/employees.json, creates temporary file.