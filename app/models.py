from typing import Optional, List, Dict

from pydantic import BaseModel


class DayScheduleBase(BaseModel):
    hr_day: Optional[str]
    classes: List[str]

class DaySchedule(DayScheduleBase):
    day: Optional[str]


class WeekSchedule(BaseModel):
    schedule: List[DayScheduleBase]