from fastapi import APIRouter
from .models import Visitor, Employee, Visit
from src.data_manager import DataManager

router = APIRouter()
dm = DataManager()

# @router.post("/visitors")
# async def add_or_update_visitor(request: Request):
#     data = await request.json()
#     visitor = Visitor(**data)
#     return dm.add_or_update_visitor(visitor)

@router.post("/visitors")
def add_or_update_visitor(visitor: Visitor):
    return dm.add_or_update_visitor(visitor)

@router.post("/employees")
def add_or_update_employee(employee: Employee):
    return dm.add_or_update_employee(employee)

@router.post("/visits")
def capture_visit(visit: Visit):
    return dm.capture_visit(visit)

@router.get("/reports/employee/{name}")
def report_by_employee(name: str):
    return dm.report_by_employee(name)

@router.get("/reports/date/{date}")
def report_by_date(date: str):
    return dm.report_by_date(date)
