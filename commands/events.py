import datetime as dt
import discord
import logging

from commands.base import Cmd
from functions import get_events

log = logging.getLogger(__name__)


help_text = """Write overview over upcoming events.
If parameter `all` is given, all events are listed even ones that are already in past.

Usage:
```<PREFIX><COMMAND> [all]```

Examples:
```<PREFIX><COMMAND>
<PREFIX><COMMAND> all```
"""

async def execute(ctx, params):
    events = get_events(ctx["guild"])
    all = False if not params or params[0].lower() != "all" else True

    if events == []:
        return True, "You don't have any events planned."
    event_list = []
    for event in sorted(events):
        if all:
            event_list.append(event)
        else:
            if event >= dt.date.today():
                event_list.append(event)
    
    if not event_list:
        if all:
            return True, "There are no events in the planner."
        else:
            return True, "There are no upcoming events planned."
        
    
    embed = discord.Embed(title = "All events:" if all else "Upcoming events:")
    for event in event_list:
        embed.add_field(name=event.title, value=event.date_time.strftime(format="%d.%m.%Y %I:%M%p"), inline=False)
    
    await ctx['channel'].send(embed=embed)

    return True, "NO RESPONSE"



command = Cmd(
    execute=execute,
    help_text="",
    params_required=0,
    team_required=True,
    admin_required=False
)

