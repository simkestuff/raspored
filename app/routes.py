from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from . import core, database, models


router = APIRouter()

#router.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("index.html", {'request': request})

@router.get("/danas", response_model=models.DayScheduleBase)
def today_timetable():
    week_number = core.get_week_no()
    schedule_type = database.get_schedule(week_number)
    today_schedule = database.get_schedule_for(core.day_name(), schedule_type)
    return today_schedule


@router.get("/sutra", response_model=models.DayScheduleBase)
def tomorrow_timetable():
    week_number = core.get_week_no(False)
    schedule_type = database.get_schedule(week_number)
    tomorrow_schedule = database.get_schedule_for(core.day_name(False), schedule_type)
    return tomorrow_schedule

@router.get("/tjedan/{id}", response_model=models.WeekSchedule)
def get_week(id: int):
    if id == 0:
        week_number = core.get_week_no()
    elif id == 1:
        week_number = core.get_week_no() + 1
    schedule_type = database.get_schedule(week_number)
    return models.WeekSchedule(schedule=database.get_week_schedule(schedule_type))
