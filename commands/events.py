import datetime as dt

import discord

from commands.base import Cmd
from functions import get_events


help_text = """Write overview over upcoming events.
If parameter `all` is given, all events are listed even ones that are already in past.

Examples:```
<PREFIX><COMMAND>
<PREFIX><COMMAND> all```
"""

async def execute(ctx, params):
    events = get_events(ctx["guild"])
    all = False if not params or params[0].lower() != "all" else True

    if events == {}:
        return True, "You don't have any events planned."
    event_list = []
    for date_time in sorted(events.keys()):
        if all:
            event_list.append((date_time, events[date_time]))
        else:
            if date_time.date() >= dt.date.today():
                event_list.append((date_time, events[date_time]))
    
    if not event_list:
        if all:
            return True, "There are no events in the planner."
        else:
            return True, "There are no upcoming events planned."
        
    
    embed = discord.Embed(title = "All events:" if all else "Upcoming events:")
    for date, name in event_list:
        embed.add_field(name=name, value=date.strftime(format="%d.%m.%Y %I:%M%p"), inline=False)
    
    await ctx['channel'].send(embed=embed)

    return True, "NO RESPONSE"



command = Cmd(
    execute=execute,
    help_text="",
    params_required=0,
    admin_required=True
)

