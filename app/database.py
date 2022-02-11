from typing import List, Optional, Dict
from pymongo import MongoClient

from .config import settings

cluster = f"mongodb+srv://{settings.database_user}:{settings.database_password}@cluster0.pdvfq.mongodb.net/{settings.database_name}?retryWrites=true&w=majority"
client = MongoClient(cluster)
db = client.timetable
days = db.days
schedules = db.schedules


def get_schedule(from_week: int) -> Optional[str]:
    """
    Given week number function connects to database and return schedule name (e.g. 'A') for that week.
    Return None if schedule for given week does not exists in database.
    """
    try:
        for schedule in schedules.find():
            if from_week in schedule["weeks"]:
                return schedule["name"]

    except:
        raise Exception()

    return None


def get_schedule_for(day_name: str, schedule_name: str):
    """
    Connects to database and return schedule for given day name and schedule name.
    Return value is list of classes or None.
    """
    try:
        class_list = days.find_one({"day" : day_name, "week_type": schedule_name}, {"hr_day": 1, "classes": 1, "_id": 0})
        return class_list
    except:
        raise Exception()
    
    return None


def get_week_schedule(week_type: str):
    res = []
    try:
        for day in days.find({"week_type": week_type}, {"_id": 0}):
            res.append(day)
        return res
    except:
        raise Exception()
    
    return None