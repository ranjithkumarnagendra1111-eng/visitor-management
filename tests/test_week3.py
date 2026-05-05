import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.week3.database import DatabaseManager, init_db
from pathlib import Path
import os

@pytest.fixture(scope="module")
def test_db():
    """Create a test database."""
    db_path = Path("test_visitor_management.db")
    init_db(db_path)
    db = DatabaseManager(db_path)
    yield db
    db.close()
    if db_path.exists():
        os.remove(db_path)

@pytest.fixture
def week3_client():
    """Test client for week3 endpoints."""
    with TestClient(app) as client:
        # Login to get token
        response = client.post("/v1/login", json={"username": "admin", "password": "password"})
        assert response.status_code == 200
        token = response.json()["access_token"]
        client.headers.update({"Authorization": f"Bearer {token}"})
        yield client

def test_login_success(week3_client):
    """Test successful login."""
    response = week3_client.post("/v1/login", json={"username": "admin", "password": "password"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_failure():
    """Test failed login."""
    client = TestClient(app)
    response = client.post("/v1/login", json={"username": "wrong", "password": "wrong"})
    assert response.status_code == 401

def test_create_employee(week3_client):
    """Test creating employee data."""
    data = {"name": "Test Employee", "department": "Test Dept", "role": "Tester"}
    response = week3_client.post("/v1/employees", json=data)
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert isinstance(response.json()["data"]["id"], int)

def test_get_employees(week3_client):
    """Test fetching employees."""
    response = week3_client.get("/v1/employees")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_employee(week3_client):
    """Test fetching a specific employee."""
    response = week3_client.post("/v1/employees", json={"name": "Jane Doe", "department": "HR", "role": "Manager"})
    assert response.status_code == 200
    employee_id = response.json()["data"]["id"]

    response = week3_client.get(f"/v1/employees/{employee_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Jane Doe"

def test_update_employee(week3_client):
    """Test updating an employee."""
    response = week3_client.post("/v1/employees", json={"name": "Bob Smith", "department": "IT", "role": "Dev"})
    employee_id = response.json()["data"]["id"]

    update_data = {"department": "Engineering"}
    response = week3_client.put(f"/v1/employees/{employee_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["success"] is True

    response = week3_client.get(f"/v1/employees/{employee_id}")
    assert response.status_code == 200
    assert response.json()["department"] == "Engineering"

def test_delete_employee(week3_client):
    """Test deleting an employee."""
    response = week3_client.post("/v1/employees", json={"name": "Alice Johnson", "department": "Sales", "role": "Rep"})
    # breakpoint()
    employee_id = response.json()["data"]["id"]

    response = week3_client.delete(f"/v1/employees/{employee_id}")
    assert response.status_code == 200
    assert response.json()["success"] is True

    response = week3_client.get(f"/v1/employees/{employee_id}")
    assert response.status_code == 404

def test_create_visitor(week3_client):
    """Test creating visitor data."""
    response = week3_client.post("/v1/visitors", json={"visitorName": "Test Visitor", "company": "Test Co", "purpose": "Test Visit", "checkInTime": "2024-01-01 10:00:00", "hostEmployeeId": 1})
    # assert response.status_code == 200
    assert response.json()["success"] is True
    assert isinstance(response.json()["data"]["id"], int)

def test_get_visitors(week3_client):
    """Test fetching visitors."""
    response = week3_client.post("/v1/visitors", json={"visitorName": "Another Visitor", "company": "Test Co", "purpose": "Meeting", "checkInTime": "2024-01-02 11:00:00", "hostEmployeeId": 1})
    assert response.status_code == 200

    response = week3_client.get("/v1/visitors")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_visit(week3_client):
    """Test creating visit data."""
    employee = week3_client.post("/v1/employees", json={"name": "Visit Host", "department": "Ops", "role": "Host"}).json()["data"]["id"]
    visitor = week3_client.post("/v1/visitors", json={"visitorName": "Visit Guest", "company": "Guest Co", "purpose": "Demo", "checkInTime": "2024-01-01 12:00:00", "hostEmployeeId": employee}).json()["data"]["id"]

    response = week3_client.post("/v1/visits", json={"visitor_id": visitor, "employee_id": employee, "check_in_time": "2024-01-01 12:00:00", "purpose": "Meeting"})
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_get_visits(week3_client):
    """Test fetching visits."""
    employee = week3_client.post("/v1/employees", json={"name": "Visit Host2", "department": "Ops", "role": "Host"}).json()["data"]["id"]
    visitor = week3_client.post("/v1/visitors", json={"visitorName": "Visit Guest2", "company": "Guest Co", "purpose": "Demo", "checkInTime": "2024-01-01 12:00:00", "hostEmployeeId": employee}).json()["data"]["id"]
    week3_client.post("/v1/visits", json={"visitor_id": visitor, "employee_id": employee, "check_in_time": "2024-01-01 12:00:00", "purpose": "Meeting"})

    response = week3_client.get("/v1/visits")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_visit_report(week3_client):
    """Test fetching visit report."""
    employee = week3_client.post("/v1/employees", json={"name": "Report Host", "department": "Ops", "role": "Host"}).json()["data"]["id"]
    visitor = week3_client.post("/v1/visitors", json={"visitorName": "Report Guest", "company": "Guest Co", "purpose": "Demo", "checkInTime": "2024-01-01 12:00:00", "hostEmployeeId": employee}).json()["data"]["id"]
    week3_client.post("/v1/visits", json={"visitor_id": visitor, "employee_id": employee, "check_in_time": "2024-01-01 12:00:00", "purpose": "Meeting"})

    response = week3_client.get("/v1/reports/visits")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_invalid_employee_payload(week3_client):
    """Test invalid employee creation payload."""
    response = week3_client.post("/v1/employees", json={"department": "Test"})
    assert response.status_code == 422

def test_unauthorized_access():
    """Test accessing endpoints without token."""
    client = TestClient(app)
    response = client.get("/v1/employees")
    assert response.status_code == 401