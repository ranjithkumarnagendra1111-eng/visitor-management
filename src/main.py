from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from src import routes
from src.week1 import routes as week1_routes
from src.week2 import routes as week2_routes
from src.week3 import routes as week3_routes
import logging

logging.basicConfig(filename="logs/app.log", level=logging.INFO)

app = FastAPI(
    title="Visitor Management",
    description="A comprehensive visitor management system with SQL database integration",
    version="1.0.0"
)

# Include routers
# app.include_router(routes.router)
app.include_router(week1_routes.router)
app.include_router(week2_routes.router)
app.include_router(week3_routes.router)

# Error handling middleware
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

