from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Team:
    id: str
    name: str
    code: str
    icon: str
    created: datetime
    member_count: int


@dataclass
class Goal:
    team_id: str
    distance: int
    units: str
    start_date: datetime
    end_date: datetime


@dataclass
class Activity:
    name: str
    type: str
    distance: float
    units: str
    duration: timedelta
    time_completed: datetime

    user_id: str
    user_first_name: str
    user_last_name: str
    user_icon: str
