import discord
import re
import datetime as dt
import logging
import traceback

from commands.base import Cmd
from functions import add_event, get_events
from lib.errors import CommandError
from lib.event import Event

log = logging.getLogger(__name__)


help_text = f'''Add a new event entry to the calendar.

The message needs to include a title followed by a time and optionally a date. \
Is no date parameter given, the current date is assumed.
Time is not time zone sensitive.

Usage:
```
<PREFIX><COMMAND> <event_title> on <event_date> at <event_time>
<PREFIX><COMMAND> <event_title> at <event_time> [on <event_date>]
```\

Examples:
```
<PREFIX><COMMAND> Scrim against Team on 22.05.2021 at 07:00pm
<PREFIX><COMMAND> The end of the world! at 07:00 pm on 21.12.2012
<PREFIX><COMMAND> Training at 07:00AM
```'''


async def execute(ctx, params):
    guild: discord.Guild = ctx['guild']
    string = ctx["params_str"]

    settings = ctx['settings']
    events_channel_id = settings['events_channel']
    team_role_id = settings['team_role']

    events_channel = guild.get_channel(events_channel_id) if events_channel_id is not None else False
    team_role = guild.get_role(team_role_id) if team_role_id is not None else False


    # create regular expression and parse date and time input
    time_re = r"at ([01]\d:\d\d) ?(am|AM|pm|PM)"
    date_re = r"on ([0123]\d[.][01]?\d[.](\d\d\d\d))"
    pattern = f"^(.*?) ({date_re} {time_re}|{time_re}( {date_re})?)$"
    p = re.compile(pattern)

    match = re.match(p, string)

    if not match:
        raise CommandError(f"Parameters for command `{ctx['prefix']}{ctx['command']}` don't match the format. Please try again or see help.")
    
    data = {
        "title": match.group(1),
        "date1": match.group(3),
        "time1": match.group(5),
        "period1": match.group(6),
        "time2": match.group(7),
        "period2": match.group(8),
        "date2": match.group(10)
    }
    title = data["title"]
    date = data["date1"] if data["date1"] else (data["date2"] if data["date2"] else dt.date.today().strftime("%d.%m.%Y"))
    time = data["time1"] if data["time1"] else data["time2"]
    period = data["period1"] if data["period1"] else data["period2"]
    
    date_time = dt.datetime.strptime(f"{date} {time}{period}", "%d.%m.%Y %I:%M%p")


    if any(event == date_time for event in get_events(guild)):
        # already an event planed for this time
        raise CommandError(f"There is already an event scheduled for {date_time}.")

    event = Event(title, date_time)
    
    if events_channel:
        content = str(event)
        if settings['event_creation_ping'] and team_role:
            content += f" {team_role.mention}"
        msg = await events_channel.send(content=content)
        event.add_message(msg)

    try:
        add_event(guild, event)
    except Exception as e:
        log.error(f"Exception during saving of event to database: {traceback.format_exc()}")
        try:
            await msg.delete()
        except NameError:
            pass
        raise CommandError("Error during event creation.")

    reply = f"{event} was added." 
    if events_channel and settings['event_creation_ping'] and not team_role:
        reply += "\nTeam role was not pinged because no or an invalid role is stored in settings."
    return reply





command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=3,
    team_required=True,
    admin_required=False
)
