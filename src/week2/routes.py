from fastapi import APIRouter, HTTPException
from .models import Visitor, Employee, Visit
from .data_manager import DataManager

router = APIRouter(prefix="/week2", tags=["Week2"])
dm = DataManager()

# Visitor Endpoints
@router.post("/visitors/add")
def add_visitor(visitor: Visitor):
    """Add a new visitor. Phone number must be unique."""
    try:
        return dm.add_visitor(visitor)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/visitors/update")
def update_visitor(visitor: Visitor):
    """Update an existing visitor by phone number."""
    try:
        return dm.update_visitor(visitor)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Employee Endpoints
@router.post("/employees/add")
def add_employee(employee: Employee):
    """Add a new employee. Phone number must be unique."""
    try:
        return dm.add_employee(employee)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/employees/update")
def update_employee(employee: Employee):
    """Update an existing employee by phone number."""
    try:
        return dm.update_employee(employee)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/visits")
def capture_visit(visit: Visit):
    return dm.capture_visit(visit)

@router.get("/reports/employee/{name}")
def report_by_employee(name: str):
    return dm.report_by_employee(name)

@router.get("/reports/date/{date}")
def report_by_date(date: str):
    return dm.report_by_date(date)
