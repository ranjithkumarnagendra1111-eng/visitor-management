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
