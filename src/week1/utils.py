import csv
import json
import logging
import tempfile
import os
from src.config import config
 
class DataManager:
    def read_employees_from_csv(self):
        """Read employees from CSV file."""
        employees = []
        try:
            with open(config.employees_csv, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    employees.append(row)
            logging.info(f"Successfully read {len(employees)} employees from CSV")
            return employees
        except FileNotFoundError as e:
            logging.error(f"CSV file not found: {config.employees_csv}")
            raise
        except Exception as e:
            logging.error(f"Error reading CSV file: {e}")
            raise
 
    def write_employees_to_json(self, employees):
        """Write employees to JSON file (persistent storage)."""
        try:
            with open(config.employees_json, "w", encoding="utf-8") as f:
                json.dump(employees, f, indent=4)
            logging.info(f"Successfully wrote {len(employees)} employees to JSON: {config.employees_json}")
            return config.employees_json
        except Exception as e:
            logging.error(f"Error writing to JSON file: {e}")
            raise
 
    def create_temp_employees_file(self, employees):
        """Create a temporary JSON file with employee data."""
        try:
            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".json", encoding="utf-8") as tmp:
                json.dump(employees, tmp, indent=4)
                temp_path = tmp.name
            logging.info(f"Created temporary file: {temp_path}")
            return temp_path
        except Exception as e:
            logging.error(f"Error creating temporary file: {e}")
            raise
 
    def ingest_bulk_employees(self):
        """Orchestrate the ingestion process: read CSV, write to JSON, create temp file."""
        try:
            # Step 1: Read employees from CSV
            employees = self.read_employees_from_csv()
 
            # Step 2: Write to JSON (persistent storage)
            json_path = self.write_employees_to_json(employees)
 
            # Step 3: Create temporary file with the same data
            temp_path = self.create_temp_employees_file(employees)
 
            logging.info(f"Ingestion completed: {len(employees)} employees processed")
            return {
                "message": f"{len(employees)} employees ingested",
                "json_file": str(json_path),
                "temp_file": temp_path
            }
 
        except Exception as e:
            logging.error(f"Error during bulk employee ingestion: {e}")
            raise

    def greet_person(self, name: str, age: int):
        """ function with parameter passing."""
        return {"greeting": f"Hello {name}, you are {age} years old!"}

    def safe_division(self, a: float, b: float):
        """safe division with error handling."""
        if b == 0:
            raise ValueError("Division by zero")
        return a / b

    def basic_file_operations(self):
        """ basic file read/write operations."""
        sample_data = {"message": "Sample file content", "timestamp": "2024-01-01"}
        
        # Write to temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            json.dump(sample_data, tmp)
            temp_path = tmp.name
        
        # Read from temp file
        with open(temp_path, 'r') as f:
            read_data = json.load(f)
        
        # Clean up
        os.unlink(temp_path)
        
        return {
            "written_data": sample_data,
            "read_data": read_data,
            "temp_file_used": True
        }
