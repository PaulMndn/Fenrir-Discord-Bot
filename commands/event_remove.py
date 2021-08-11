import datetime as dt
import logging

from commands.base import Cmd
from functions import rem_event


help_text = """Remove event from event planner.
Event is identified by date and time.
Tip: Simply copy & paste the time from the events overview behind the command.

Usage: `<PREFIX><COMMAND> <date> <time>`

date: format: dd.mm.yyyy
time: format: hh:mm"AM"/"PM"

Example: `<PREFIX><COMMAND> 23.05.2021 07:00PM`
"""


async def execute(ctx, params):
    logging.info(f"Executing command {ctx['command']} {ctx['params_str']}.")
    guild = ctx["guild"]
    date = params[0]
    time = params[1]
    
    try:
        date_time = dt.datetime.strptime(f"{date} {time}", "%d.%m.%Y %I:%M%p")
    except ValueError:
        logging.error(f"Invalide parameter format for date and time: {date} {time}.")
        return False, "Date and/or time format was not recognized."

    success, event = rem_event(guild, date_time)
    if success:
        return True, f"Event *{event}* was removed from the event planner."
    else:
        return False, f"No event is planned for {date} {time}."


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=2,
    admin_required=True
)


