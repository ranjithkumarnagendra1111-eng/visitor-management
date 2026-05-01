from fastapi import FastAPI
from src import routes
from src.week1 import routes as week1_routes
from src.week2 import routes as week2_routes
import logging

logging.basicConfig(filename="logs/app.log", level=logging.INFO)

app = FastAPI(title="Visitor Management")

# app.include_router(routes.router)
app.include_router(week1_routes.router)
app.include_router(week2_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to Visitor Management"}

