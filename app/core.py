from datetime import datetime, timedelta


def get_week_no(today: bool = True) -> int:
    """Return week number for today's date.
    If var today equal to False, return week number for tomorrow date.
    """
    query_date = datetime.today()
    if not today:
       query_date = query_date + timedelta(days=1)

    _, week_no, _ = query_date.isocalendar()

    return week_no 


def day_name(today: bool = True) -> str:
   """
   Return day name for today (e.g. like Monday).
   If var today is false, return tomorrow day name.
   """
   if today:
      return datetime.today().strftime("%A")
   else:
      return (datetime.today() + timedelta(days=1)).strftime("%A")