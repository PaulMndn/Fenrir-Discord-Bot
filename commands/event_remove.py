import datetime as dt

from commands.base import Cmd
from functions import get_events
from utils import write_db


async def execute(ctx, params):
    guild = ctx["guild"]
    date = params[0]
    time = params[1]
    
    events = get_events(guild)
    event = dt.datetime.strptime(f"{date} {time}", "%d.%m.%Y %I:%M%p")

    if not event in events:
        return False, "At the specified time is no event planned."
    del_event = events[event]
    del(events[event])

    if not write_db(guild, "events", events):
        return False, f"Event {del_event} on {event.strftime('%d.%m.%Y %I:%M%p')} could not be deleted from database."

    return True, f"Event {del_event} on {event.strftime('%d.%m.%Y %I:%M%p')} was deleted."

command = Cmd(
    execute=execute,
    help_text="",
    params_required=2,
    admin_required=True
)


