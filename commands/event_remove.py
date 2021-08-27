import discord
import datetime as dt
import logging

from commands.base import Cmd
from utils import get_guild_settings
from functions import rem_event

log = logging.getLogger(__name__)


help_text = """Remove event from event planner.
Event is identified by date and time.
Tip: Simply copy & paste the time from the events overview behind the command.

Usage: 
```<PREFIX><COMMAND> <event_date> <event_time>```
date format: dd.mm.yyyy
time format: hh:mm"AM"/"PM"

Example: 
```<PREFIX><COMMAND> 23.05.2021 07:00PM```
"""


async def execute(ctx, params):
    guild: discord.Guild = ctx["guild"]
    date = params[0]
    time = params[1]
    
    try:
        date_time = dt.datetime.strptime(f"{date} {time}", "%d.%m.%Y %I:%M%p")
    except ValueError:
        log.error(f"Invalide parameter format for date and time: {date} {time}.")
        return False, "Date and/or time format was not recognized."

    success, event = rem_event(guild, date_time)
    try:
        await guild.get_channel(event.event_channel_id).get_partial_message(event.msg_id).delete()
    except discord.NotFound:
        log.warning(f"Event message for event '{event}' in planner channel \
            ({guild.get_channel(event.event_channel_id).name} <#{event.event_channel_id}>) \
            was not found and could not be deleted.")
        await ctx['channel'].send(f"Event message was not found in event planner (<#{event.event_channel_id}>) and thus could not be deleted.")

    
    if success:
        return True, f"Event {event} was removed from the event planner."
    else:
        return False, f"No event is planned for {date} {time}."


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=2,
    team_required=True,
    admin_required=False
)


