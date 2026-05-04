import json
from pathlib import Path

import pytest
from src.week1.utils import DataManager


@pytest.fixture
def sample_employees():
    return [
        {"id": "1", "name": "John Doe", "department": "Engineering"},
        {"id": "2", "name": "Jane Smith", "department": "HR"}
    ]


@pytest.fixture
def temp_csv_path(tmp_path: Path, sample_employees):
    csv_path = tmp_path / "employees.csv"
    csv_path.write_text(
        "id,name,department\n"
        + "\n".join(
            f"{row['id']},{row['name']},{row['department']}" for row in sample_employees
        ),
        encoding="utf-8",
    )
    return csv_path


@pytest.fixture
def patched_week1_config(tmp_path: Path, monkeypatch, temp_csv_path: Path):
    from src import config

    json_path = tmp_path / "employees.json"
    json_path.write_text("[]", encoding="utf-8")

    monkeypatch.setattr(config.config, "employees_csv", temp_csv_path)
    monkeypatch.setattr(config.config, "employees_json", json_path)

    return json_path


def test_data_manager_ingest_bulk_employees(patched_week1_config, sample_employees):
    dm = DataManager()

    result = dm.ingest_bulk_employees()

    assert "ingested" in result["message"]
    assert result["temp_file"].endswith('.json')

    with open(patched_week1_config, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == len(sample_employees)
    assert data[0]["name"] == sample_employees[0]["name"]

    temp_file = Path(result["temp_file"])
    if temp_file.exists():
        temp_file.unlink()