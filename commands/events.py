import datetime as dt
import discord
import logging
import math
import re

from commands.base import Cmd
from functions import get_events
from utils import add_react_msg, none_func

log = logging.getLogger(__name__)


help_text = """Write overview over upcoming events.
If parameter `all` is given, all events are listed even ones that are already in past.

Usage:
```<PREFIX><COMMAND> [all]```\

Examples:
```<PREFIX><COMMAND>
<PREFIX><COMMAND> all```
"""

async def scroll(reaction, user):
    guild = reaction.message.guild
    msg = reaction.message
    embed = reaction.message.embeds[0]
    m = re.match(r"Page (\d+) of \d+.", embed.description)
    current_page = int(m.group(1))
    events = sorted(get_events(guild))
    last_page = math.ceil(len(events)/10)

    if reaction.emoji == "⬇":
        new_page = current_page+1 if current_page+1 <= last_page else last_page
        embed.description = f"Page {new_page} of {last_page}."
        embed.clear_fields()
        try:
            for e in events[(new_page-1)*10:new_page*10]:
                embed.add_field(name=e.title, value=e.date_time.strftime(format="%d.%m.%Y %I:%M%p"), inline=False)
        except IndexError:
            pass
        await msg.edit(content="", embed=embed)

    elif reaction.emoji == "⬆":
        new_page = current_page-1 if current_page-1 >= 1 else 1
        embed.description = f"Page {new_page} of {last_page}."
        embed.clear_fields()
        try:
            for e in events[(new_page-1)*10:new_page*10]:
                embed.add_field(name=e.title, value=e.date_time.strftime(format="%d.%m.%Y %I:%M%p"), inline=False)
        except IndexError:
            pass
        await msg.edit(content="", embed=embed)

    else:
        await reaction.clear()
        return
    await reaction.remove(user)


async def execute(ctx, params):
    events = get_events(ctx["guild"])
    all = False if not params or params[0].lower() != "all" else True

    if events == []:
        return "You don't have any events planned."
    event_list = []
    for event in sorted(events):
        if all:
            event_list.append(event)
        else:
            if event >= dt.date.today():
                event_list.append(event)
    
    if not event_list:
        if all:
            return "There are no events in the planner."
        else:
            return "There are no upcoming events planned."
    
    embed = discord.Embed(title = "All events" if all else "Upcoming events")

    if all:
        overflow = False
        if len(event_list) <= 10:
            for event in event_list:
                embed.add_field(name=event.title, value=event.date_time.strftime(format="%d.%m.%Y %I:%M%p"), inline=False)
        else:
            overflow = True
            last_page = math.ceil(len(event_list)/10)
            event_list = event_list[(len(event_list)//10)*10:]
            embed.description = f"Page {last_page} of {last_page}."
            for event in event_list:
                embed.add_field(name=event.title, value=event.date_time.strftime(format="%d.%m.%Y %I:%M%p"), inline=False)

        
    else:
        if len(event_list) > 10:
            event_list = event_list[:10]
            embed.description = "Next 10 events."
        for event in event_list:
            embed.add_field(name=event.title, value=event.date_time.strftime(format="%d.%m.%Y %I:%M%p"), inline=False)

    msg = await ctx['channel'].send(embed=embed)
    if all and overflow:
        await msg.add_reaction("⬆")
        await msg.add_reaction("⬇")
        add_react_msg(ctx['guild'], msg, scroll, none_func)





command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    team_required=True,
    admin_required=False
)

