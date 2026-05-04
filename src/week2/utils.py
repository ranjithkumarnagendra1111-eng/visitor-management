import json
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pathlib import Path
from typing import Any, Dict, List

from src.config import config
from .interfaces import DataLoader, Transformer, Writer


class SingletonMeta(type):
    _instances: Dict[type, Any] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigManager(metaclass=SingletonMeta):
    def __init__(self):
        self.data_dir: Path = config.data_dir
        self.visitors_file: Path = config.visitors_json
        self.employees_file: Path = config.employees_json
        self.visits_file: Path = config.visits_json

    def to_dict(self) -> Dict[str, str]:
        return {
            "data_dir": str(self.data_dir),
            "visitors_file": str(self.visitors_file),
            "employees_file": str(self.employees_file),
            "visits_file": str(self.visits_file),
        }


class VisitorDataLoader(DataLoader):
    def load_data(self, source: str) -> List[Dict[str, Any]]:
        if source == "visitors":
            return [
                {"visitorName": "Rahul Verma", "visitorPhoneNumber": "9876543210", "comingFrom": "Bangalore"},
                {"visitorName": "Priya Iyer", "visitorPhoneNumber": "9876501234", "comingFrom": "Chennai"},
            ]
        if source == "employees":
            return [
                {"employeeName": "Anita Sharma", "department": "HR", "phoneNumber": "9123456789"},
                {"employeeName": "Ramesh Kumar", "department": "IT", "phoneNumber": "9988776655"},
            ]
        raise ValueError(f"Unknown source: {source}")


class VisitorTransformer(Transformer):
    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        transformed: List[Dict[str, Any]] = []
        for record in data:
            transformed.append(
                {
                    **record,
                    "visitorName": record.get("visitorName", "").title(),
                    "reviewed": True,
                    "summary": "Visitor cleared for entry" if record.get("visitorName") else "Visitor record created",
                }
            )
        return transformed


class JsonWriter(Writer):
    def write(self, data: List[Dict[str, Any]], destination: str) -> str:
        with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".json", prefix=f"{destination}_", encoding="utf-8") as tmp:
            json.dump(data, tmp, indent=2)
            return str(Path(tmp.name).resolve())


class VisitorManagementPipeline:
    def __init__(self, loader: DataLoader, transformer: Transformer, writer: Writer):
        self.loader = loader
        self.transformer = transformer
        self.writer = writer

    def run(self, source: str) -> Dict[str, Any]:
        raw_data = self.loader.load_data(source)
        transformed = self.transformer.transform(raw_data)
        output = self.writer.write(transformed, source)
        return {
            "source": source,
            "records_loaded": len(raw_data),
            "records_transformed": len(transformed),
            "output_file": output,
            "sample_transformed": transformed[:1],
        }


def _cpu_task(value: int) -> int:
    return value * value


class ConcurrencyExplorer:
    def compare_threading_vs_multiprocessing(self, values: List[int]) -> Dict[str, Any]:
        results: Dict[str, Any] = {}

        start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=4) as executor:
            _ = list(executor.map(_cpu_task, values))
        results["threading_duration"] = time.perf_counter() - start

        start = time.perf_counter()
        with ProcessPoolExecutor(max_workers=4) as executor:
            _ = list(executor.map(_cpu_task, values))
        results["multiprocessing_duration"] = time.perf_counter() - start

        results["values_count"] = len(values)
        return results

    def parallel_file_processing(self, datasets: List[List[Dict[str, Any]]]) -> Dict[str, Any]:
        def write_dataset(dataset: List[Dict[str, Any]]) -> str:
            with tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".json", prefix="visitor_dataset_", encoding="utf-8") as tmp:
                json.dump(dataset, tmp, indent=2)
                return str(Path(tmp.name).resolve())

        start = time.perf_counter()
        with ThreadPoolExecutor(max_workers=3) as executor:
            paths = list(executor.map(write_dataset, datasets))
        duration = time.perf_counter() - start
        return {
            "method": "threading_file_processing",
            "duration_sec": duration,
            "files_created": paths,
        }
