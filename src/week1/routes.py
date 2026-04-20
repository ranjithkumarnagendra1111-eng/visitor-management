from fastapi import APIRouter, HTTPException
import logging
from src.week1.utils import DataManager

router = APIRouter(prefix="/week1", tags=["Week1"])
dm = DataManager()

@router.post("/ingest_bulk_employees")
def ingest_bulk_employees():
    try:
        result = dm.ingest_bulk_employees()
        return result
    except Exception as e:
        logging.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data-types-mutability")
def demonstrate_data_types_mutability():
    """Demonstrates data types and mutability with examples."""
    try:
        # Immutable types
        immutable_str = "Hello"
        immutable_int = 42
        immutable_tuple = (1, 2, 3)
        
        # Mutable types
        mutable_list = [1, 2, 3]
        mutable_dict = {"key": "value"}
        
        # Show mutability
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
                "tuple": immutable_tuple
            },
            "mutable_examples": {
                "list_original": original_list,
                "list_modified": mutable_list,
                "list_changed": mutable_list_changed,
                "dict_original": original_dict,
                "dict_modified": mutable_dict,
                "dict_changed": mutable_dict_changed
            }
        }
    except Exception as e:
        logging.error(f"Error in data types demo: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/functions-parameter-passing/{name}/{age}")
def demonstrate_functions_parameter_passing(name: str, age: int):
    """Demonstrates functions and parameter passing."""
    try:
        result = dm.greet_person(name, age)
        logging.info(f"Function called with params: name={name}, age={age}")
        return result
    except Exception as e:
        logging.error(f"Error in function demo: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/error-handling/{trigger_error}")
def demonstrate_error_handling(trigger_error: bool = False):
    """Demonstrates error handling with optional error triggering."""
    try:
        if trigger_error:
            raise ValueError("This is a sample error for demonstration")
        
        result = dm.safe_division(10, 2)
        logging.info("Error handling demo completed successfully")
        return {"result": result, "error_triggered": False}
    except Exception as e:
        logging.error(f"Handled error in demo: {e}")
        return {"error": str(e), "error_triggered": True, "handled": True}

@router.get("/logging-demo")
def demonstrate_logging():
    """Demonstrates logging (vs print) with different levels."""
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
def demonstrate_file_handling():
    """Demonstrates basic file handling operations."""
    try:
        result = dm.basic_file_operations()
        logging.info("File handling demo completed")
        return result
    except Exception as e:
        logging.error(f"Error in file handling demo: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/project-structure-modules")
def demonstrate_project_structure_modules():
    """Demonstrates project structure and module usage."""
    try:
        import src.config
        import src.week1.utils
        
        modules_info = {
            "config_module": str(src.config),
            "utils_module": str(src.week1.utils),
            "data_manager_class": str(DataManager),
            "config_paths": {
                "data_dir": str(src.config.config.data_dir),
                "employees_csv": str(src.config.config.employees_csv)
            }
        }
        
        logging.info("Project structure and modules demo")
        return modules_info
    except Exception as e:
        logging.error(f"Error in project structure demo: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/virtual-environments")
def demonstrate_virtual_environments():
    """Demonstrates virtual environment awareness."""
    try:
        import sys
        import os
        
        venv_info = {
            "python_executable": sys.executable,
            "python_version": sys.version,
            "current_working_directory": os.getcwd(),
            "is_in_venv": sys.prefix != sys.base_prefix,
            "venv_prefix": sys.prefix,
            "base_prefix": sys.base_prefix
        }
        
        logging.info("Virtual environment demo")
        return venv_info
    except Exception as e:
        logging.error(f"Error in virtual environment demo: {e}")
        raise HTTPException(status_code=500, detail=str(e))
