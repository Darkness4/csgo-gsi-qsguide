from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class DataStore:
    """Pass data to the ui."""

    data: Optional[Dict[str, Any]] = None
