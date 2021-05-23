import datetime as dt

from commands.base import Cmd
from functions import get_events
from utils import write_db


help_text = """Remove event from planner.
Event is identified by date and time.
Tip: Simply copy & paste the time from the events overview behind the command.

Usage: `<PREFIX><COMMAND> <date> <time>`

date: format: dd.mm.yyyy
time: format: hh:mm"AM"/"PM"

Example: `<PREFIX><COMMAND> 23.05.2021 07:00PM`
"""


async def execute(ctx, params):
    guild = ctx["guild"]
    date = params[0]
    time = params[1]
    
    events = get_events(guild)
    try:
        date_time = dt.datetime.strptime(f"{date} {time}", "%d.%m.%Y %I:%M%p")
    except ValueError:
        return False, "Date and/or time format was not recognized."

    if not date_time in events:
        return True, "At the specified time is no event planned."
    del_event_name = events[date_time]
    del(events[date_time])

    if not write_db(guild, "events", events):
        return False, f"Event {del_event_name} on {date_time.strftime('%d.%m.%Y %I:%M%p')} could not be deleted from database."

    return True, f"Event {del_event_name} on {date_time.strftime('%d.%m.%Y %I:%M%p')} was deleted."

command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=2,
    admin_required=True
)


