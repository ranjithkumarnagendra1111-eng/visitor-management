from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from src import routes
import logging
from pathlib import Path

log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)
logging.basicConfig(filename="logs/app.log", level=logging.INFO)

app = FastAPI(
    title="Visitor Management",
    description="A comprehensive visitor management system with SQL database integration",
    version="1.0.0"
)

app.include_router(routes.router)

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "Internal server error"}
    )

@app.get("/")
def root():
    return {"message": "Welcome to Visitor Management"}
