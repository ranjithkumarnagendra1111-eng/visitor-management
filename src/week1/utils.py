import csv
import json
import logging
import tempfile
import os
from src.config import config

class DataManager:
    def ingest_bulk_employees(self):
        employees = []
        try:
            # Read CSV
            with open(config.employees_csv, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    employees.append(row)

            # Write to JSON (persistent storage)
            with open(config.employees_json, "w", encoding="utf-8") as f:
                json.dump(employees, f, indent=4)

            # Temporary file handling (demo)
            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".json") as tmp:
                json.dump(employees, tmp, indent=4)
                temp_path = tmp.name

            logging.info(f"Ingested {len(employees)} employees from CSV")
            return {"message": f"{len(employees)} employees ingested", "temp_file": temp_path}

        except Exception as e:
            logging.error(f"Error ingesting employees: {e}")
            raise

    def greet_person(self, name: str, age: int):
        """Demonstrates function with parameter passing."""
        return {"greeting": f"Hello {name}, you are {age} years old!"}

    def safe_division(self, a: float, b: float):
        """Demonstrates safe division with error handling."""
        if b == 0:
            raise ValueError("Division by zero")
        return a / b

    def basic_file_operations(self):
        """Demonstrates basic file read/write operations."""
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
