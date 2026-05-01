import os
from pathlib import Path
 
BASE_DIR = Path(__file__).parent.parent
 
class Config:
    def __init__(self):
        self.data_dir = BASE_DIR / "data"
        self.employees_csv = self.data_dir / "employees.csv"
        self.employees_json = self.data_dir / "employees.json"
        self.visitors_json = self.data_dir / "visitors.json"
        self.visits_json = self.data_dir / "visits.json"
        self.log_file = BASE_DIR / "logs" / "app.log"
        self.output_dir = BASE_DIR / "output"
 
config = Config()