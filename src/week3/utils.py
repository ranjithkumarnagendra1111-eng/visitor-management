from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
from .database import DatabaseManager
from .models import Employee, Visitor, Visit

logger = logging.getLogger(__name__)

class DataService:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    def create_employee(self, employee: Employee) -> int:
        """Create a new employee record."""
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

    def create_visitor(self, visitor: Visitor) -> int:
        """Create a new visitor record."""
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

    def create_visit(self, visit: Visit) -> int:
        """Create a new visit record."""
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
        """Fetch all employees."""
        rows = self.db.fetch_all("SELECT * FROM employees ORDER BY name")
        return [dict(row) for row in rows]

    def get_employee(self, employee_id: int) -> Optional[Dict[str, Any]]:
        """Fetch a specific employee."""
        row = self.db.fetch_one("SELECT * FROM employees WHERE id = ?", (employee_id,))
        return dict(row) if row else None

    def update_employee(self, employee_id: int, updates: Dict[str, Any]) -> bool:
        """Update an employee."""
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
        """Delete an employee."""
        self.db.execute_query("DELETE FROM employees WHERE id = ?", (employee_id,))
        return True

    def get_visitors(self) -> List[Dict[str, Any]]:
        """Fetch all visitors."""
        rows = self.db.fetch_all("SELECT * FROM visitors ORDER BY visitorName")
        return [dict(row) for row in rows]

    def get_visitor(self, visitor_id: int) -> Optional[Dict[str, Any]]:
        """Fetch a specific visitor."""
        row = self.db.fetch_one("SELECT * FROM visitors WHERE id = ?", (visitor_id,))
        return dict(row) if row else None

    def update_visitor(self, visitor_id: int, updates: Dict[str, Any]) -> bool:
        """Update a visitor."""
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
        """Delete a visitor."""
        self.db.execute_query("DELETE FROM visitors WHERE id = ?", (visitor_id,))
        return True

    def get_visits(self) -> List[Dict[str, Any]]:
        """Fetch all visits."""
        rows = self.db.fetch_all("SELECT * FROM visits ORDER BY check_in_time DESC")
        return [dict(row) for row in rows]

    def get_visit(self, visit_id: int) -> Optional[Dict[str, Any]]:
        """Fetch a specific visit."""
        row = self.db.fetch_one("SELECT * FROM visits WHERE id = ?", (visit_id,))
        return dict(row) if row else None

    def update_visit(self, visit_id: int, updates: Dict[str, Any]) -> bool:
        """Update a visit."""
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
        """Delete a visit."""
        self.db.execute_query("DELETE FROM visits WHERE id = ?", (visit_id,))
        return True

    def get_visit_report(self) -> List[Dict[str, Any]]:
        """Get a report of visits with joins."""
        rows = self.db.fetch_all("""
            SELECT v.id, vis.visitorName, e.name as employee_name, v.check_in_time, v.check_out_time, v.purpose
            FROM visits v
            INNER JOIN visitors vis ON v.visitor_id = vis.id
            INNER JOIN employees e ON v.employee_id = e.id
            ORDER BY v.check_in_time DESC
        """)
        return [dict(row) for row in rows]