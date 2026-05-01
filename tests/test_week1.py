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


def test_data_manager_ingest_bulk_employees():
    """Test the ingest_bulk_employees method with temporary files."""
    dm = DataManager()

    # Create a temporary CSV file with sample data
    sample_data = [
        {"id": "1", "name": "John Doe", "department": "Engineering"},
        {"id": "2", "name": "Jane Smith", "department": "HR"}
    ]

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_csv:
        tmp_csv.write("id,name,department\n")
        for row in sample_data:
            tmp_csv.write(f"{row['id']},{row['name']},{row['department']}\n")
        tmp_csv_path = tmp_csv.name

    # Temporarily override config paths
    from src import config
    original_csv = config.config.employees_csv
    original_json = config.config.employees_json
    config.config.employees_csv = tmp_csv_path
    config.config.employees_json = tmp_csv_path.replace('.csv', '.json')

    try:
        result = dm.ingest_bulk_employees()
        assert "ingested" in result["message"]
        assert result["temp_file"].endswith('.json')

        # Check if JSON was written
        with open(config.config.employees_json, 'r') as f:
            data = json.load(f)
            assert len(data) == 2
            assert data[0]["name"] == "John Doe"

    finally:
        # Restore original config
        config.config.employees_csv = original_csv
        config.config.employees_json = original_json
        # Clean up temp files
        os.unlink(tmp_csv_path)
        if os.path.exists(config.config.employees_json):
            os.unlink(config.config.employees_json)
        if 'temp_file' in result and os.path.exists(result['temp_file']):
            os.unlink(result['temp_file'])