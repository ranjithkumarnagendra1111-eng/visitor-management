import json
import logging
from pathlib import Path
from src.config import config

class DataManager:
    def __init__(self):
        self.visitors_file = config.visitors_json
        self.employees_file = config.employees_json
        self.visits_file = config.visits_json

    def _read(self, file):
        try:
            if file.exists():
                with open(file, "r") as f:
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
            with open(file, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            logging.error(f"Error writing {file}: {e}")
            raise

    def add_visitor(self, visitor):
        """Add a new visitor. Phone number must be unique."""
        visitors = self._read(self.visitors_file)
        for v in visitors:
            if v["visitorPhoneNumber"] == visitor.visitorPhoneNumber:
                raise ValueError(f"Visitor with phone number {visitor.visitorPhoneNumber} already exists")
        visitors.append(visitor.dict())
        self._write(self.visitors_file, visitors)
        return {"message": "Visitor added successfully", "data": visitor.dict()}

    def update_visitor(self, visitor):
        """Update an existing visitor by phone number."""
        visitors = self._read(self.visitors_file)
        for v in visitors:
            if v["visitorPhoneNumber"] == visitor.visitorPhoneNumber:
                v.update(visitor.dict())
                self._write(self.visitors_file, visitors)
                return {"message": "Visitor updated successfully", "data": v}
        raise ValueError(f"Visitor with phone number {visitor.visitorPhoneNumber} not found")

    def add_employee(self, employee):
        """Add a new employee. Phone number must be unique."""
        employees = self._read(self.employees_file)
        for e in employees:
            if e["phoneNumber"] == employee.phoneNumber:
                raise ValueError(f"Employee with phone number {employee.phoneNumber} already exists")
        employees.append(employee.dict())
        self._write(self.employees_file, employees)
        return {"message": "Employee added successfully", "data": employee.dict()}

    def update_employee(self, employee):
        """Update an existing employee by phone number."""
        employees = self._read(self.employees_file)
        for e in employees:
            if e["phoneNumber"] == employee.phoneNumber:
                e.update(employee.dict())
                self._write(self.employees_file, employees)
                return {"message": "Employee updated successfully", "data": e}
        raise ValueError(f"Employee with phone number {employee.phoneNumber} not found")

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
        return "Visit recorded"

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
