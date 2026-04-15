import json
import logging
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

class DataManager:
    def __init__(self):
        self.visitors_file = DATA_DIR / "visitors.json"
        self.employees_file = DATA_DIR / "employees.json"
        self.visits_file = DATA_DIR / "visits.json"

    def _read(self, file):
        try:
            if file.exists():
                with open(file, "r") as f:
                    return json.load(f)
            return []
        except Exception as e:
            logging.error(f"Error reading {file}: {e}")
            raise

    def _write(self, file, data):
        try:
            with open(file, "w") as f:
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
                return "Visitor updated"
        visitors.append(visitor.dict())
        self._write(self.visitors_file, visitors)
        return "Visitor added"

    def add_or_update_employee(self, employee):
        employees = self._read(self.employees_file)
        for e in employees:
            if e["phoneNumber"] == employee.phoneNumber:
                e.update(employee.dict())
                self._write(self.employees_file, employees)
                return "Employee updated"
        employees.append(employee.dict())
        self._write(self.employees_file, employees)
        return "Employee added"

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
