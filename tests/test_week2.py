import pytest
from pathlib import Path

from fastapi.testclient import TestClient
import src.config as config_mod
from src.main import app
from src.week2 import routes as week2_routes
from src.week2.data_manager import DataManager


def _setup_temp_data(tmp_path: Path):
    visitors_file = tmp_path / "visitors.json"
    employees_file = tmp_path / "employees.json"
    visits_file = tmp_path / "visits.json"
    visitors_file.write_text("[]")
    employees_file.write_text("[]")
    visits_file.write_text("[]")
    return visitors_file, employees_file, visits_file


@pytest.fixture
def week2_client(tmp_path, monkeypatch):
    visitors_file, employees_file, visits_file = _setup_temp_data(tmp_path)
    monkeypatch.setattr(config_mod.config, "visitors_json", visitors_file)
    monkeypatch.setattr(config_mod.config, "employees_json", employees_file)
    monkeypatch.setattr(config_mod.config, "visits_json", visits_file)
    week2_routes.dm = DataManager()
    return TestClient(app)


@pytest.fixture
def visitor_payload():
    return {
        "visitorName": "Rahul Verma",
        "visitorPhoneNumber": "9876543210",
        "visitorDriverLicenseNumber": "DL1234567890",
        "visitorCompanyName": "Acme Corp",
        "comingFrom": "Bangalore"
    }


@pytest.fixture
def employee_payload():
    return {
        "employeeName": "Anita Sharma",
        "department": "HR",
        "phoneNumber": "9123456789",
        "designation": "Recruiter"
    }


@pytest.fixture
def visit_payload(visitor_payload, employee_payload):
    return {
        "visitDate": "2026-05-01",
        "visitorPhoneNumber": visitor_payload["visitorPhoneNumber"],
        "employeePhoneNumber": employee_payload["phoneNumber"],
        "purposeOfVisit": "Interview",
        "visitDuration": 120,
        "comments": "Visitor arrived early"
    }


def test_add_and_update_visitor(week2_client, visitor_payload):
    add_response = week2_client.post("/week2/visitors/add", json=visitor_payload)
    assert add_response.status_code == 200
    assert add_response.json()["message"] == "Visitor added successfully"

    updated_payload = visitor_payload.copy()
    updated_payload["visitorCompanyName"] = "Acme Solutions"

    update_response = week2_client.put("/week2/visitors/update", json=updated_payload)
    assert update_response.status_code == 200
    assert update_response.json()["message"] == "Visitor updated successfully"
    assert update_response.json()["data"]["visitorCompanyName"] == "Acme Solutions"


def test_add_and_update_employee(week2_client, employee_payload):
    add_response = week2_client.post("/week2/employees/add", json=employee_payload)
    assert add_response.status_code == 200
    assert add_response.json()["message"] == "Employee added successfully"

    updated_payload = employee_payload.copy()
    updated_payload["designation"] = "Lead Recruiter"

    update_response = week2_client.put("/week2/employees/update", json=updated_payload)
    assert update_response.status_code == 200
    assert update_response.json()["message"] == "Employee updated successfully"
    assert update_response.json()["data"]["designation"] == "Lead Recruiter"


def test_capture_visit_and_reports(week2_client, visitor_payload, employee_payload, visit_payload):
    visitor_response = week2_client.post("/week2/visitors/add", json=visitor_payload)
    assert visitor_response.status_code == 200

    employee_response = week2_client.post("/week2/employees/add", json=employee_payload)
    assert employee_response.status_code == 200

    visit_response = week2_client.post("/week2/visits", json=visit_payload)
    assert visit_response.status_code == 200
    assert visit_response.json() == "Visit recorded"

    employee_report = week2_client.get("/week2/reports/employee/Anita%20Sharma")
    assert employee_report.status_code == 200
    employee_data = employee_report.json()
    assert isinstance(employee_data, list)
    assert len(employee_data) == 1
    assert employee_data[0]["visitorPhoneNumber"] == visitor_payload["visitorPhoneNumber"]
    assert employee_data[0]["purposeOfVisit"] == visit_payload["purposeOfVisit"]

    date_report = week2_client.get(f"/week2/reports/date/{visit_payload['visitDate']}")
    assert date_report.status_code == 200
    date_data = date_report.json()
    assert isinstance(date_data, list)
    assert len(date_data) == 1
    assert date_data[0]["visitDate"] == visit_payload["visitDate"]
    assert date_data[0]["employeePhoneNumber"] == employee_payload["phoneNumber"]
    assert date_data[0]["visitorPhoneNumber"] == visitor_payload["visitorPhoneNumber"]
