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

@router.get("/dan/{id}", response_model=models.DayScheduleBase, response_class=HTMLResponse)
def today_timetable(id: int, request: Request):
    danas = True
    if id == 1:
        danas = False

    week_number = core.get_week_no(danas)
    schedule_type = database.get_schedule(week_number)

    schedule = database.get_schedule_for(core.day_name(danas), schedule_type)

    if schedule:
        sch_mod = models.DayScheduleBase(**schedule)
        return templates.TemplateResponse("dan.html", {'request': request, 'dan': sch_mod.hr_day, 'sati': sch_mod.classes})
    else:
        return templates.TemplateResponse("no_data.html", {'request': request})



# @router.get("/sutra", response_model=models.DayScheduleBase)
# def tomorrow_timetable():
#     week_number = core.get_week_no(False)
#     schedule_type = database.get_schedule(week_number)
#     tomorrow_schedule = database.get_schedule_for(core.day_name(False), schedule_type)
#     return tomorrow_schedule

@router.get("/tjedan/{id}", response_model=models.WeekSchedule)
def get_week(id: int, request: Request):
    if id == 0:
        week_number = core.get_week_no()
    elif id == 1:
        week_number = core.get_week_no() + 1
    schedule_type = database.get_schedule(week_number)

    week_schedule = models.WeekSchedule(schedule=database.get_week_schedule(schedule_type))

    return templates.TemplateResponse("week.html", {'request': request, 'week_list': week_schedule.schedule})

    #return models.WeekSchedule(schedule=database.get_week_schedule(schedule_type))
