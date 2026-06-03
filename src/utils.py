import csv
import json
import logging
import tempfile
import os
import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.config import config
from src.database import DatabaseManager
from .models import EmployeeDB, VisitorDB, VisitDB

class DataIngestionManager:
    def read_employees_from_csv(self):
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
        try:
            with open(config.employees_json, "w", encoding="utf-8") as f:
                json.dump(employees, f, indent=4)
            logging.info(f"Successfully wrote {len(employees)} employees to JSON: {config.employees_json}")
            return config.employees_json
        except Exception as e:
            logging.error(f"Error writing to JSON file: {e}")
            raise

    def create_temp_employees_file(self, employees):
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
        try:
            employees = self.read_employees_from_csv()
            json_path = self.write_employees_to_json(employees)
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
        return {"greeting": f"Hello {name}, you are {age} years old!"}

    def safe_division(self, a: float, b: float):
        if b == 0:
            raise ValueError("Division by zero")
        return a / b

    def basic_file_operations(self):
        sample_data = {"message": "Sample file content", "timestamp": "2024-01-01"}
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            json.dump(sample_data, tmp)
            temp_path = tmp.name
        with open(temp_path, 'r') as f:
            read_data = json.load(f)
        os.unlink(temp_path)
        return {
            "written_data": sample_data,
            "read_data": read_data,
            "temp_file_used": True
        }

class JsonDataManager:
    def __init__(self):
        self.visitors_file = config.visitors_json
        self.employees_file = config.employees_json
        self.visits_file = config.visits_json

    def _read(self, file):
        try:
            if file.exists():
                with open(file, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        return json.loads(content)
            return []
        except json.JSONDecodeError:
            logging.warning(f"Empty or invalid JSON in {file}, returning empty list")
            return []
        except Exception as e:
            logging.error(f"Error reading {file}: {e}")
            raise

    def _write(self, file, data):
        try:
            file.parent.mkdir(parents=True, exist_ok=True)
            with open(file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logging.error(f"Error writing {file}: {e}")
            raise

    def add_or_update_visitor(self, visitor):
        visitors = self._read(self.visitors_file)
        for v in visitors:
            if v["visitorPhoneNumber"] == visitor.visitorPhoneNumber:
                v.update(visitor.dict())
                self._write(self.visitors_file, visitors)
                return {"message": "Visitor updated", "data": v}
        visitors.append(visitor.dict())
        self._write(self.visitors_file, visitors)
        return {"message": "Visitor added", "data": visitor.dict()}

    def add_or_update_employee(self, employee):
        employees = self._read(self.employees_file)
        for e in employees:
            if e["phoneNumber"] == employee.phoneNumber:
                e.update(employee.dict())
                self._write(self.employees_file, employees)
                return {"message": "Employee updated", "data": e}
        employees.append(employee.dict())
        self._write(self.employees_file, employees)
        return {"message": "Employee added", "data": employee.dict()}

    def capture_visit(self, visit):
        visitors = self._read(self.visitors_file)
        employees = self._read(self.employees_file)
        if not any(v["visitorPhoneNumber"] == visit.visitorPhoneNumber for v in visitors):
            raise ValueError("Visitor not found")
        if not any(e["phoneNumber"] == visit.employeePhoneNumber for e in employees):
            raise ValueError("Employee not found")
        visits = self._read(self.visits_file)
        visits.append(visit.dict())
        self._write(self.visits_file, visits)
        return {"message": "Visit recorded", "data": visit.dict()}

    def add_visitor(self, visitor):
        visitors = self._read(self.visitors_file)
        for v in visitors:
            if v["visitorPhoneNumber"] == visitor.visitorPhoneNumber:
                raise ValueError(f"Visitor with phone number {visitor.visitorPhoneNumber} already exists")
        visitors.append(visitor.dict())
        self._write(self.visitors_file, visitors)
        return {"message": "Visitor added successfully", "data": visitor.dict()}

    def update_visitor(self, visitor):
        visitors = self._read(self.visitors_file)
        for v in visitors:
            if v["visitorPhoneNumber"] == visitor.visitorPhoneNumber:
                v.update(visitor.dict())
                self._write(self.visitors_file, visitors)
                return {"message": "Visitor updated successfully", "data": v}
        raise ValueError(f"Visitor with phone number {visitor.visitorPhoneNumber} not found")

    def add_employee(self, employee):
        employees = self._read(self.employees_file)
        for e in employees:
            if e["phoneNumber"] == employee.phoneNumber:
                raise ValueError(f"Employee with phone number {employee.phoneNumber} already exists")
        employees.append(employee.dict())
        self._write(self.employees_file, employees)
        return {"message": "Employee added successfully", "data": employee.dict()}

    def update_employee(self, employee):
        employees = self._read(self.employees_file)
        for e in employees:
            if e["phoneNumber"] == employee.phoneNumber:
                e.update(employee.dict())
                self._write(self.employees_file, employees)
                return {"message": "Employee updated successfully", "data": e}
        raise ValueError(f"Employee with phone number {employee.phoneNumber} not found")

    def report_by_employee(self, name):
        employees = self._read(self.employees_file)
        visits = self._read(self.visits_file)
        visitors = self._read(self.visitors_file)
        result = []
        for e in employees:
            if e["employeeName"].lower() == name.lower():
                for v in visits:
                    if v["employeePhoneNumber"] == e["phoneNumber"]:
                        visitor_info = next((vis for vis in visitors if vis["visitorPhoneNumber"] == v["visitorPhoneNumber"]), {})
                        result.append({**visitor_info, **v})
        if not result:
            return {"error": "Employee not found or no visitors"}
        return result

    def report_by_date(self, date):
        visits = self._read(self.visits_file)
        visitors = self._read(self.visitors_file)
        employees = self._read(self.employees_file)
        result = []
        for v in visits:
            if v["visitDate"] == date:
                visitor_info = next((vis for vis in visitors if vis["visitorPhoneNumber"] == v["visitorPhoneNumber"]), {})
                employee_info = next((emp for emp in employees if emp["phoneNumber"] == v["employeePhoneNumber"]), {})
                result.append({**visitor_info, **employee_info, **v})
        if not result:
            return {"error": "No visits found for this date"}
        return result

class DataLoader(ABC):
    @abstractmethod
    def load_data(self, source: str) -> List[Dict[str, Any]]:
        pass

class Transformer(ABC):
    @abstractmethod
    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        pass

class Writer(ABC):
    @abstractmethod
    def write(self, data: List[Dict[str, Any]], destination: str) -> str:
        pass

class SingletonMeta(type):
    _instances: Dict[type, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class ConfigManager(metaclass=SingletonMeta):
    def __init__(self):
        self.data_dir: Path = config.data_dir
        self.visitors_file: Path = config.visitors_json
        self.employees_file: Path = config.employees_json
        self.visits_file: Path = config.visits_json

    def to_dict(self) -> Dict[str, str]:
        return {
            "data_dir": str(self.data_dir),
            "visitors_file": str(self.visitors_file),
            "employees_file": str(self.employees_file),
            "visits_file": str(self.visits_file),
        }

class VisitorDataLoader(DataLoader):
    def load_data(self, source: str) -> List[Dict[str, Any]]:
        if source == "visitors":
            return [
                {"visitorName": "Rahul Verma", "visitorPhoneNumber": "9876543210", "comingFrom": "Bangalore"},
                {"visitorName": "Priya Iyer", "visitorPhoneNumber": "9876501234", "comingFrom": "Chennai"},
            ]
        if source == "employees":
            return [
                {"employeeName": "Anita Sharma", "department": "HR", "phoneNumber": "9123456789"},
                {"employeeName": "Ramesh Kumar", "department": "IT", "phoneNumber": "9988776655"},
            ]
        raise ValueError(f"Unknown source: {source}")

class VisitorTransformer(Transformer):
    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        transformed: List[Dict[str, Any]] = []
        for record in data:
            transformed.append(
                {
                    **record,
                    "visitorName": record.get("visitorName", "").title(),
                    "reviewed": True,
                    "summary": "Visitor cleared for entry" if record.get("visitorName") else "Visitor record created",
                }
            )
        return transformed

class JsonWriter(Writer):
    def write(self, data: List[Dict[str, Any]], destination: str) -> str:
        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".json", prefix=f"{destination}_", encoding="utf-8") as tmp:
            json.dump(data, tmp, indent=2)
            return str(Path(tmp.name).resolve())

class VisitorManagementPipeline:
    def __init__(self, loader: DataLoader, transformer: Transformer, writer: Writer):
        self.loader = loader
        self.transformer = transformer
        self.writer = writer

    def run(self, source: str) -> Dict[str, Any]:
        raw_data = self.loader.load_data(source)
        transformed = self.transformer.transform(raw_data)
        output = self.writer.write(transformed, source)
        return {
            "source": source,
            "records_loaded": len(raw_data),
            "records_transformed": len(transformed),
            "output_file": output,
            "sample_transformed": transformed[:1],
        }

class ConcurrencyExplorer:
    def compare_threading_vs_multiprocessing(self, values: List[int]) -> Dict[str, Any]:
        results: Dict[str, Any] = {}

        start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=4) as executor:
            _ = list(executor.map(lambda v: v * v, values))
        results["threading_duration"] = time.perf_counter() - start

        start = time.perf_counter()
        with ProcessPoolExecutor(max_workers=4) as executor:
            _ = list(executor.map(lambda v: v * v, values))
        results["multiprocessing_duration"] = time.perf_counter() - start

        results["values_count"] = len(values)
        return results

    def parallel_file_processing(self, datasets: List[List[Dict[str, Any]]]) -> Dict[str, Any]:
        def write_dataset(dataset: List[Dict[str, Any]]) -> str:
            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".json", prefix="visitor_dataset_", encoding="utf-8") as tmp:
                json.dump(dataset, tmp, indent=2)
                return str(Path(tmp.name).resolve())

        start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=3) as executor:
            paths = list(executor.map(write_dataset, datasets))
        duration = time.perf_counter() - start
        return {
            "method": "threading_file_processing",
            "duration_sec": duration,
            "files_created": paths,
        }

class DataService:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def create_employee(self, employee: EmployeeDB) -> int:
        if employee.id is not None:
            cursor = self.db.execute_query(
                "INSERT OR REPLACE INTO employees (id, name, department, role) VALUES (?, ?, ?, ?)",
                (employee.id, employee.name, employee.department, employee.role)
            )
        else:
            cursor = self.db.execute_query(
                "INSERT INTO employees (name, department, role) VALUES (?, ?, ?)",
                (employee.name, employee.department, employee.role)
            )
        return cursor.lastrowid if cursor else employee.id

    def create_visitor(self, visitor: VisitorDB) -> int:
        if visitor.id is not None:
            cursor = self.db.execute_query(
                "INSERT OR REPLACE INTO visitors (id, visitorName, company, purpose, checkInTime, checkOutTime, hostEmployeeId) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (visitor.id, visitor.visitorName, visitor.company, visitor.purpose,
                 visitor.checkInTime, visitor.checkOutTime, visitor.hostEmployeeId)
            )
        else:
            cursor = self.db.execute_query(
                "INSERT INTO visitors (visitorName, company, purpose, checkInTime, checkOutTime, hostEmployeeId) VALUES (?, ?, ?, ?, ?, ?)",
                (visitor.visitorName, visitor.company, visitor.purpose,
                 visitor.checkInTime, visitor.checkOutTime, visitor.hostEmployeeId)
            )
        return cursor.lastrowid if cursor else visitor.id

    def create_visit(self, visit: VisitDB) -> int:
        if visit.id is not None:
            cursor = self.db.execute_query(
                "INSERT OR REPLACE INTO visits (id, visitor_id, employee_id, check_in_time, check_out_time, purpose) VALUES (?, ?, ?, ?, ?, ?)",
                (visit.id, visit.visitor_id, visit.employee_id, visit.check_in_time,
                 visit.check_out_time, visit.purpose)
            )
        else:
            cursor = self.db.execute_query(
                "INSERT INTO visits (visitor_id, employee_id, check_in_time, check_out_time, purpose) VALUES (?, ?, ?, ?, ?)",
                (visit.visitor_id, visit.employee_id, visit.check_in_time,
                 visit.check_out_time, visit.purpose)
            )
        return cursor.lastrowid if cursor else visit.id

    def get_employees(self) -> List[Dict[str, Any]]:
        rows = self.db.fetch_all("SELECT * FROM employees ORDER BY name")
        return [dict(row) for row in rows]

    def get_employee(self, employee_id: int) -> Optional[Dict[str, Any]]:
        row = self.db.fetch_one("SELECT * FROM employees WHERE id = ?", (employee_id,))
        return dict(row) if row else None

    def update_employee(self, employee_id: int, updates: Dict[str, Any]) -> bool:
        set_parts = []
        params = []
        for key, value in updates.items():
            if value is not None:
                set_parts.append(f"{key} = ?")
                params.append(value)
        if not set_parts:
            return False
        params.append(employee_id)
        query = f"UPDATE employees SET {', '.join(set_parts)} WHERE id = ?"
        self.db.execute_query(query, tuple(params))
        return True

    def delete_employee(self, employee_id: int) -> bool:
        self.db.execute_query("DELETE FROM employees WHERE id = ?", (employee_id,))
        return True

    def get_visitors(self) -> List[Dict[str, Any]]:
        rows = self.db.fetch_all("SELECT * FROM visitors ORDER BY visitorName")
        return [dict(row) for row in rows]

    def get_visitor(self, visitor_id: int) -> Optional[Dict[str, Any]]:
        row = self.db.fetch_one("SELECT * FROM visitors WHERE id = ?", (visitor_id,))
        return dict(row) if row else None

    def update_visitor(self, visitor_id: int, updates: Dict[str, Any]) -> bool:
        set_parts = []
        params = []
        for key, value in updates.items():
            if value is not None:
                set_parts.append(f"{key} = ?")
                params.append(value)
        if not set_parts:
            return False
        params.append(visitor_id)
        query = f"UPDATE visitors SET {', '.join(set_parts)} WHERE id = ?"
        self.db.execute_query(query, tuple(params))
        return True

    def delete_visitor(self, visitor_id: int) -> bool:
        self.db.execute_query("DELETE FROM visitors WHERE id = ?", (visitor_id,))
        return True

    def get_visits(self) -> List[Dict[str, Any]]:
        rows = self.db.fetch_all("SELECT * FROM visits ORDER BY check_in_time DESC")
        return [dict(row) for row in rows]

    def get_visit(self, visit_id: int) -> Optional[Dict[str, Any]]:
        row = self.db.fetch_one("SELECT * FROM visits WHERE id = ?", (visit_id,))
        return dict(row) if row else None

    def update_visit(self, visit_id: int, updates: Dict[str, Any]) -> bool:
        set_parts = []
        params = []
        for key, value in updates.items():
            if value is not None:
                set_parts.append(f"{key} = ?")
                params.append(value)
        if not set_parts:
            return False
        params.append(visit_id)
        query = f"UPDATE visits SET {', '.join(set_parts)} WHERE id = ?"
        self.db.execute_query(query, tuple(params))
        return True

    def delete_visit(self, visit_id: int) -> bool:
        self.db.execute_query("DELETE FROM visits WHERE id = ?", (visit_id,))
        return True

    def get_visit_report(self) -> List[Dict[str, Any]]:
        rows = self.db.fetch_all("""
            SELECT v.id, vis.visitorName, e.name as employee_name, v.check_in_time, v.check_out_time, v.purpose
            FROM visits v
            INNER JOIN visitors vis ON v.visitor_id = vis.id
            INNER JOIN employees e ON v.employee_id = e.id
            ORDER BY v.check_in_time DESC
        """)
        return [dict(row) for row in rows]
