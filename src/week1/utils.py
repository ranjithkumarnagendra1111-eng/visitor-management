import csv
import json
import logging
import tempfile
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
