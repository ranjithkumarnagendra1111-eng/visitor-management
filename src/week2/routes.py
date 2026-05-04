from fastapi import APIRouter, HTTPException
from .models import Visitor, Employee, Visit
from .data_manager import DataManager
from .utils import (
    ConfigManager,
    VisitorDataLoader,
    VisitorTransformer,
    JsonWriter,
    VisitorManagementPipeline,
    ConcurrencyExplorer,
)

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


@router.get("/singleton-config-manager")
def singleton_config_manager():
    """Demonstrate the singleton config manager for Week 2."""
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
    """Demonstrate interface-based visitor management design."""
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
    """Write multiple visitor datasets in parallel using threading."""
    explorer = ConcurrencyExplorer()
    datasets = [
        [
            {"visitorName": "Rahul Verma", "visitorPhoneNumber": "9876543210", "comingFrom": "Bangalore"},
            {"visitorName": "Priya Iyer", "visitorPhoneNumber": "9876501234", "comingFrom": "Chennai"},
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
    """Compare threading and multiprocessing for a visitor-count workload."""
    explorer = ConcurrencyExplorer()
    values = list(range(1, 41))
    result = explorer.compare_threading_vs_multiprocessing(values)
    return {
        "component": "Concurrency comparison",
        "description": "Compare threading and multiprocessing for a small visitor processing task",
        "result": result,
    }
