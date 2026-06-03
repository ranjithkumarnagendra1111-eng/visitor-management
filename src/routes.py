from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
import sys
import os

from .models import (
    VisitorBase, EmployeeBase, VisitBase,
    EmployeeDB, VisitorDB, VisitDB,
    CreateEmployeeRequest, CreateVisitorRequest,
    CreateVisitRequest, UpdateEmployeeRequest,
    UpdateVisitorRequest, UpdateVisitRequest,
    StandardResponse, TokenResponse, LoginRequest
)
from .utils import (
    DataIngestionManager, JsonDataManager,
    ConfigManager, VisitorDataLoader,
    VisitorTransformer, JsonWriter,
    VisitorManagementPipeline,
    ConcurrencyExplorer, DataService
)
from .database import DatabaseManager, init_db

router = APIRouter()

# Managers for different examples
data_ingestion_manager = DataIngestionManager()
json_manager = JsonDataManager()
config_manager = ConfigManager()

db_path = Path(__file__).parent.parent / "data" / "visitor_management.db"
init_db(db_path)
db_manager = DatabaseManager(db_path)
data_service = DataService(db_manager)

VALID_TOKENS = {"secret-token-123"}
security = HTTPBearer(auto_error=False)


def verify_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)):
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


@router.get("/")
def root():
    return {"message": "Welcome to Visitor Management"}


# Root JSON manager endpoints
@router.post("/visitors")
def add_or_update_visitor(visitor: VisitorBase):
    return json_manager.add_or_update_visitor(visitor)


@router.post("/employees")
def add_or_update_employee(employee: EmployeeBase):
    return json_manager.add_or_update_employee(employee)




@router.get("/reports/date/{date}")
def report_by_date(date: str):
    return json_manager.report_by_date(date)


# Demo endpoints
@router.post("/ingest_bulk_employees")
def ingest_bulk_employees():
    try:
        return data_ingestion_manager.ingest_bulk_employees()
    except Exception as e:
        logging.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/data-types-mutability")
def data_types_mutability():
    try:
        immutable_str = "Hello"
        immutable_int = 42
        immutable_tuple = (1, 2, 3)
        mutable_list = [1, 2, 3]
        mutable_dict = {"key": "value"}

        original_list = mutable_list.copy()
        mutable_list.append(4)
        mutable_list_changed = mutable_list != original_list

        original_dict = mutable_dict.copy()
        mutable_dict["new_key"] = "new_value"
        mutable_dict_changed = mutable_dict != original_dict

        logging.info("Demonstrated data types and mutability")
        return {
            "immutable_examples": {
                "string": immutable_str,
                "integer": immutable_int,
                "tuple": immutable_tuple,
            },
            "mutable_examples": {
                "list_original": original_list,
                "list_modified": mutable_list,
                "list_changed": mutable_list_changed,
                "dict_original": original_dict,
                "dict_modified": mutable_dict,
                "dict_changed": mutable_dict_changed,
            },
        }
    except Exception as e:
        logging.error(f"Error in data types demo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/functions-parameter-passing/{name}/{age}")
def functions_parameter_passing(name: str, age: int):
    try:
        result = data_ingestion_manager.greet_person(name, age)
        logging.info(f"Function called with params: name={name}, age={age}")
        return result
    except Exception as e:
        logging.error(f"Error in function demo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/error-handling/{trigger_error}")
def error_handling(trigger_error: bool = False):
    try:
        if trigger_error:
            raise ValueError("This is a sample error for demonstration")

        result = data_ingestion_manager.safe_division(10, 2)
        logging.info("Error handling demo completed successfully")
        return {"result": result, "error_triggered": False}
    except Exception as e:
        logging.error(f"Handled error in demo: {e}")
        return {"error": str(e), "error_triggered": True, "handled": True}


@router.get("/logging-demo")
def demo_logging():
    try:
        logging.debug("This is a debug message")
        logging.info("This is an info message - logging demo")
        logging.warning("This is a warning message")
        logging.error("This is an error message")
        return {"message": "Check logs/app.log for logged messages", "levels_demonstrated": ["debug", "info", "warning", "error"]}
    except Exception as e:
        logging.error(f"Error in logging demo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/file-handling-demo")
def demo_file_handling():
    try:
        result = data_ingestion_manager.basic_file_operations()
        logging.info("File handling demo completed")
        return result
    except Exception as e:
        logging.error(f"Error in file handling demo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/project-structure-modules")
def project_structure_modules():
    try:
        import src.config
        import src.utils

        modules_info = {
            "config_module": str(src.config),
            "utils_module": str(src.utils),
            "data_manager_class": str(DataIngestionManager),
            "config_paths": {
                "data_dir": str(src.config.config.data_dir),
                "employees_csv": str(src.config.config.employees_csv),
            },
        }

        logging.info("Project structure and modules demo")
        return modules_info
    except Exception as e:
        logging.error(f"Error in project structure demo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/virtual-environments")
def virtual_environments():
    try:
        venv_info = {
            "python_executable": sys.executable,
            "python_version": sys.version,
            "current_working_directory": os.getcwd(),
            "is_in_venv": sys.prefix != sys.base_prefix,
            "venv_prefix": sys.prefix,
            "base_prefix": sys.base_prefix,
        }

        logging.info("Virtual environment demo")
        return venv_info
    except Exception as e:
        logging.error(f"Error in virtual environment demo: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/visitors/add")
def add_visitor(visitor: VisitorBase):
    try:
        return json_manager.add_visitor(visitor)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/visitors/update")
def update_visitor(visitor: VisitorBase):
    try:
        return json_manager.update_visitor(visitor)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/employees/add")
def add_employee(employee: EmployeeBase):
    try:
        return json_manager.add_employee(employee)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/employees/update")
def update_employee(employee: EmployeeBase):
    try:
        return json_manager.update_employee(employee)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/visits")
def capture_visit(visit: VisitBase):
    try:
        return json_manager.capture_visit(visit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/singleton-config-manager")
def singleton_config_manager():
    first = ConfigManager()
    second = ConfigManager()
    return {
        "component": "Singleton ConfigManager",
        "same_instance": first is second,
        "instance_id": id(first),
        "config": first.to_dict(),
    }


@router.get("/interface-based-design")
def interface_based_design():
    loader = VisitorDataLoader()
    transformer = VisitorTransformer()
    writer = JsonWriter()
    pipeline = VisitorManagementPipeline(loader, transformer, writer)
    result = pipeline.run("visitors")
    return {
        "component": "Interface-based design",
        "description": "Sample visitor-management pipeline using Loader, Transformer, and Writer interfaces",
        "result": result,
    }


@router.get("/parallel-file-processing")
def parallel_file_processing():
    explorer = ConcurrencyExplorer()
    datasets = [
        [
            {"visitorName": "Rahul Verma", "visitorPhoneNumber": "9876543210", "comingFrom": "Bangalore"},
            {"visitorName": "Priya Iyer", "visitorPhoneNumber": "9876543214", "comingFrom": "Chennai"},
        ],
        [
            {"visitorName": "Anita Rao", "visitorPhoneNumber": "9988001122", "comingFrom": "Mumbai"},
            {"visitorName": "Vikram Singh", "visitorPhoneNumber": "9988112233", "comingFrom": "Delhi"},
        ],
        [
            {"visitorName": "Sonal Patel", "visitorPhoneNumber": "9876543211", "comingFrom": "Pune"},
        ],
    ]
    result = explorer.parallel_file_processing(datasets)
    return {
        "component": "Parallel file processing",
        "description": "Parallel visit dataset writes for visitor management",
        "result": result,
    }


@router.get("/concurrency-compare")
def concurrency_compare():
    explorer = ConcurrencyExplorer()
    values = list(range(1, 41))
    result = explorer.compare_threading_vs_multiprocessing(values)
    return {
        "component": "Concurrency comparison",
        "description": "Compare threading and multiprocessing for a small visitor processing task",
        "result": result,
    }


@router.post("/v1/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    if request.username == "admin" and request.password == "password":
        return TokenResponse(access_token="secret-token-123")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


@router.post("/v1/employees", response_model=StandardResponse, dependencies=[Depends(verify_token)])
async def create_employee(request: CreateEmployeeRequest):
    try:
        employee = EmployeeDB(**request.dict())
        new_id = data_service.create_employee(employee)
        return StandardResponse(success=True, message="Employee created successfully", data={"id": new_id})
    except Exception as e:
        logging.error(f"Error creating employee: {e}")
        raise HTTPException(status_code=500, detail="Failed to create employee")


@router.get("/v1/employees", response_model=List[Dict[str, Any]], dependencies=[Depends(verify_token)])
async def get_employees():
    try:
        return data_service.get_employees()
    except Exception as e:
        logging.error(f"Error fetching employees: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch employees")


@router.get("/v1/employees/{employee_id}", response_model=Dict[str, Any], dependencies=[Depends(verify_token)])
async def get_employee(employee_id: int):
    try:
        employee = data_service.get_employee(employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error fetching employee {employee_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch employee")


@router.put("/v1/employees/{employee_id}", response_model=StandardResponse, dependencies=[Depends(verify_token)])
async def update_employee_v1(employee_id: int, request: UpdateEmployeeRequest):
    try:
        updates = request.dict(exclude_unset=True)
        if not data_service.update_employee(employee_id, updates):
            raise HTTPException(status_code=400, detail="No valid updates provided")
        return StandardResponse(success=True, message="Employee updated successfully")
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating employee {employee_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update employee")


@router.delete("/v1/employees/{employee_id}", response_model=StandardResponse, dependencies=[Depends(verify_token)])
async def delete_employee_v1(employee_id: int):
    try:
        data_service.delete_employee(employee_id)
        return StandardResponse(success=True, message="Employee deleted successfully")
    except Exception as e:
        logging.error(f"Error deleting employee {employee_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete employee")


@router.post("/v1/visitors", response_model=StandardResponse, dependencies=[Depends(verify_token)])
async def create_visitor(request: CreateVisitorRequest):
    try:
        visitor = VisitorDB(**request.dict())
        new_id = data_service.create_visitor(visitor)
        return StandardResponse(success=True, message="Visitor created successfully", data={"id": new_id})
    except Exception as e:
        logging.error(f"Error creating visitor: {e}")
        raise HTTPException(status_code=500, detail="Failed to create visitor")


@router.get("/v1/visitors", response_model=List[Dict[str, Any]], dependencies=[Depends(verify_token)])
async def get_visitors():
    try:
        return data_service.get_visitors()
    except Exception as e:
        logging.error(f"Error fetching visitors: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch visitors")


@router.get("/v1/visitors/{visitor_id}", response_model=Dict[str, Any], dependencies=[Depends(verify_token)])
async def get_visitor(visitor_id: int):
    try:
        visitor = data_service.get_visitor(visitor_id)
        if not visitor:
            raise HTTPException(status_code=404, detail="Visitor not found")
        return visitor
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error fetching visitor {visitor_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch visitor")


@router.put("/v1/visitors/{visitor_id}", response_model=StandardResponse, dependencies=[Depends(verify_token)])
async def update_visitor_v1(visitor_id: int, request: UpdateVisitorRequest):
    try:
        updates = request.dict(exclude_unset=True)
        if not data_service.update_visitor(visitor_id, updates):
            raise HTTPException(status_code=400, detail="No valid updates provided")
        return StandardResponse(success=True, message="Visitor updated successfully")
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating visitor {visitor_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update visitor")


@router.delete("/v1/visitors/{visitor_id}", response_model=StandardResponse, dependencies=[Depends(verify_token)])
async def delete_visitor_v1(visitor_id: int):
    try:
        data_service.delete_visitor(visitor_id)
        return StandardResponse(success=True, message="Visitor deleted successfully")
    except Exception as e:
        logging.error(f"Error deleting visitor {visitor_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete visitor")


@router.post("/v1/visits", response_model=StandardResponse, dependencies=[Depends(verify_token)])
async def create_visit(request: CreateVisitRequest):
    try:
        visit = VisitDB(**request.dict())
        new_id = data_service.create_visit(visit)
        return StandardResponse(success=True, message="Visit created successfully", data={"id": new_id})
    except Exception as e:
        logging.error(f"Error creating visit: {e}")
        raise HTTPException(status_code=500, detail="Failed to create visit")


@router.get("/v1/visits", response_model=List[Dict[str, Any]], dependencies=[Depends(verify_token)])
async def get_visits():
    try:
        return data_service.get_visits()
    except Exception as e:
        logging.error(f"Error fetching visits: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch visits")


@router.get("/v1/visits/{visit_id}", response_model=Dict[str, Any], dependencies=[Depends(verify_token)])
async def get_visit(visit_id: int):
    try:
        visit = data_service.get_visit(visit_id)
        if not visit:
            raise HTTPException(status_code=404, detail="Visit not found")
        return visit
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error fetching visit {visit_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch visit")


@router.put("/v1/visits/{visit_id}", response_model=StandardResponse, dependencies=[Depends(verify_token)])
async def update_visit_v1(visit_id: int, request: UpdateVisitRequest):
    try:
        updates = request.dict(exclude_unset=True)
        if not data_service.update_visit(visit_id, updates):
            raise HTTPException(status_code=400, detail="No valid updates provided")
        return StandardResponse(success=True, message="Visit updated successfully")
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error updating visit {visit_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update visit")


@router.delete("/v1/visits/{visit_id}", response_model=StandardResponse, dependencies=[Depends(verify_token)])
async def delete_visit_v1(visit_id: int):
    try:
        data_service.delete_visit(visit_id)
        return StandardResponse(success=True, message="Visit deleted successfully")
    except Exception as e:
        logging.error(f"Error deleting visit {visit_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete visit")


@router.get("/v1/reports/visits", response_model=List[Dict[str, Any]], dependencies=[Depends(verify_token)])
async def get_visit_report():
    try:
        return data_service.get_visit_report()
    except Exception as e:
        logging.error(f"Error fetching visit report: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch visit report")
