from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
from .database import DatabaseManager, init_db
from .models import (
    Employee, Visitor, Visit, CreateEmployeeRequest, CreateVisitorRequest,
    CreateVisitRequest, UpdateEmployeeRequest, UpdateVisitorRequest,
    UpdateVisitRequest, StandardResponse, TokenResponse, LoginRequest
)
from .utils import DataService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1", tags=["Week 3 API"])

# Simple in-memory token store (in production, use proper JWT)
VALID_TOKENS = {"secret-token-123"}

security = HTTPBearer(auto_error=False)

def verify_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
    """Verify the provided token."""
    if credentials is None or credentials.credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided"
        )
    if credentials.credentials not in VALID_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
    return credentials.credentials

# Initialize database
DB_PATH = Path(__file__).parent.parent.parent / "data" / "visitor_management.db"
init_db(DB_PATH)
db_manager = DatabaseManager(DB_PATH)
data_service = DataService(db_manager)

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """Simple login endpoint - returns a token."""
    # In production, verify username/password against database
    if request.username == "admin" and request.password == "password":
        return TokenResponse(access_token="secret-token-123")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials"
    )

@router.post("/employees", response_model=StandardResponse, dependencies=[Depends(verify_token)])
async def create_employee(request: CreateEmployeeRequest):
    """Create a new employee from request payload."""
    try:
        employee = Employee(**request.dict())
        new_id = data_service.create_employee(employee)
        return StandardResponse(success=True, message="Employee created successfully", data={"id": new_id})
    except Exception as e:
        logger.error(f"Error creating employee: {e}")
        raise HTTPException(status_code=500, detail="Failed to create employee")

@router.get("/employees", response_model=List[Dict[str, Any]], dependencies=[Depends(verify_token)])
async def get_employees():
    """Fetch all employees."""
    try:
        return data_service.get_employees()
    except Exception as e:
        logger.error(f"Error fetching employees: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch employees")

@router.get("/employees/{employee_id}", response_model=Dict[str, Any], dependencies=[Depends(verify_token)])
async def get_employee(employee_id: int):
    """Fetch a specific employee."""
    try:
        employee = data_service.get_employee(employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching employee {employee_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch employee")

@router.put("/employees/{employee_id}", response_model=StandardResponse, dependencies=[Depends(verify_token)])
async def update_employee(employee_id: int, request: UpdateEmployeeRequest):
    """Update an employee."""
    try:
        updates = request.dict(exclude_unset=True)
        if not data_service.update_employee(employee_id, updates):
            raise HTTPException(status_code=400, detail="No valid updates provided")
        return StandardResponse(success=True, message="Employee updated successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating employee {employee_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update employee")

@router.delete("/employees/{employee_id}", response_model=StandardResponse, dependencies=[Depends(verify_token)])
async def delete_employee(employee_id: int):
    """Delete an employee."""
    try:
        data_service.delete_employee(employee_id)
        return StandardResponse(success=True, message="Employee deleted successfully")
    except Exception as e:
        logger.error(f"Error deleting employee {employee_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete employee")

@router.post("/visitors", response_model=StandardResponse, dependencies=[Depends(verify_token)])
async def create_visitor(request: CreateVisitorRequest):
    """Create a new visitor from request payload."""
    try:
        visitor = Visitor(**request.dict())
        new_id = data_service.create_visitor(visitor)
        return StandardResponse(success=True, message="Visitor created successfully", data={"id": new_id})
    except Exception as e:
        logger.error(f"Error creating visitor: {e}")
        raise HTTPException(status_code=500, detail="Failed to create visitor")

@router.get("/visitors", response_model=List[Dict[str, Any]], dependencies=[Depends(verify_token)])
async def get_visitors():
    """Fetch all visitors."""
    try:
        return data_service.get_visitors()
    except Exception as e:
        logger.error(f"Error fetching visitors: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch visitors")

@router.get("/visitors/{visitor_id}", response_model=Dict[str, Any], dependencies=[Depends(verify_token)])
async def get_visitor(visitor_id: int):
    """Fetch a specific visitor."""
    try:
        visitor = data_service.get_visitor(visitor_id)
        if not visitor:
            raise HTTPException(status_code=404, detail="Visitor not found")
        return visitor
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching visitor {visitor_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch visitor")

@router.put("/visitors/{visitor_id}", response_model=StandardResponse, dependencies=[Depends(verify_token)])
async def update_visitor(visitor_id: int, request: UpdateVisitorRequest):
    """Update a visitor."""
    try:
        updates = request.dict(exclude_unset=True)
        if not data_service.update_visitor(visitor_id, updates):
            raise HTTPException(status_code=400, detail="No valid updates provided")
        return StandardResponse(success=True, message="Visitor updated successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating visitor {visitor_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update visitor")

@router.delete("/visitors/{visitor_id}", response_model=StandardResponse, dependencies=[Depends(verify_token)])
async def delete_visitor(visitor_id: int):
    """Delete a visitor."""
    try:
        data_service.delete_visitor(visitor_id)
        return StandardResponse(success=True, message="Visitor deleted successfully")
    except Exception as e:
        logger.error(f"Error deleting visitor {visitor_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete visitor")

@router.post("/visits", response_model=StandardResponse, dependencies=[Depends(verify_token)])
async def create_visit(request: CreateVisitRequest):
    """Create a new visit from request payload."""
    try:
        visit = Visit(**request.dict())
        new_id = data_service.create_visit(visit)
        return StandardResponse(success=True, message="Visit created successfully", data={"id": new_id})
    except Exception as e:
        logger.error(f"Error creating visit: {e}")
        raise HTTPException(status_code=500, detail="Failed to create visit")

@router.get("/visits", response_model=List[Dict[str, Any]], dependencies=[Depends(verify_token)])
async def get_visits():
    """Fetch all visits."""
    try:
        return data_service.get_visits()
    except Exception as e:
        logger.error(f"Error fetching visits: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch visits")

@router.get("/visits/{visit_id}", response_model=Dict[str, Any], dependencies=[Depends(verify_token)])
async def get_visit(visit_id: int):
    """Fetch a specific visit."""
    try:
        visit = data_service.get_visit(visit_id)
        if not visit:
            raise HTTPException(status_code=404, detail="Visit not found")
        return visit
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching visit {visit_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch visit")

@router.put("/visits/{visit_id}", response_model=StandardResponse, dependencies=[Depends(verify_token)])
async def update_visit(visit_id: int, request: UpdateVisitRequest):
    """Update a visit."""
    try:
        updates = request.dict(exclude_unset=True)
        if not data_service.update_visit(visit_id, updates):
            raise HTTPException(status_code=400, detail="No valid updates provided")
        return StandardResponse(success=True, message="Visit updated successfully")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating visit {visit_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update visit")

@router.delete("/visits/{visit_id}", response_model=StandardResponse, dependencies=[Depends(verify_token)])
async def delete_visit(visit_id: int):
    """Delete a visit."""
    try:
        data_service.delete_visit(visit_id)
        return StandardResponse(success=True, message="Visit deleted successfully")
    except Exception as e:
        logger.error(f"Error deleting visit {visit_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete visit")

@router.get("/reports/visits", response_model=List[Dict[str, Any]], dependencies=[Depends(verify_token)])
async def get_visit_report():
    """Get a report of visits with visitor and employee details."""
    try:
        return data_service.get_visit_report()
    except Exception as e:
        logger.error(f"Error fetching visit report: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch visit report")