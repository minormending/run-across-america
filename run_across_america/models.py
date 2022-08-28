from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict


@dataclass
class Team:
    id: str
    name: str
    code: str
    icon: str
    created: datetime
    member_count: int
