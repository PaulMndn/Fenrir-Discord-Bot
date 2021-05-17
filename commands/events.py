import datetime as dt

import discord

from commands.base import Cmd
from functions import get_events



async def execute(ctx, params):
    events = get_events(ctx["guild"])
    if events == {}:
        return True, "You don't have any events planned."
    upcoming = []
    for k, v in events.items():
        if k.date() >= dt.date.today():
            upcoming.append((k, v))
    if upcoming == []:
        return True, "There are no upcoming events planned."
    
    embed = discord.Embed(title="Upcoming events:")
    for date, name in upcoming:
        embed.add_field(name=name, value=date.strftime(format="%d.%m.%Y %I:%M%p"), inline=False)
    
    await ctx['channel'].send(embed=embed)

    return True, "NO RESPONSE"



command = Cmd(
    execute=execute,
    help_text="",
    params_required=0,
    admin_required=True
)