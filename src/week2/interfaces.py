from abc import ABC, abstractmethod
from typing import Any, List, Dict

class DataLoader(ABC):
    """Abstract base class for data loading components."""

    @abstractmethod
    def load_data(self, source: str) -> List[Dict[str, Any]]:
        """Load data from a source and return as list of dictionaries."""
        pass

class Transformer(ABC):
    """Abstract base class for data transformation components."""

    @abstractmethod
    def transform(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform the input data and return transformed data."""
        pass

class Writer(ABC):
    """Abstract base class for data writing components."""

    @abstractmethod
    def write(self, data: List[Dict[str, Any]], destination: str) -> str:
        """Write data to a destination and return the destination path."""
        pass