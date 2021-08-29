import discord
# import commands
from . import (
    availability,
    event_add,
    event_remove,
    events,
    help,
    history,
    ping,
    potato,
    settings,
)



commands = {
    "availability": availability.command,
    "add-event": event_add.command,
    "events": events.command,
    "help": help.command,
    "history": history.command,
    "ping": ping.command,
    "potato": potato.command,
    "remove-event": event_remove.command,
    "settings": settings.command
}

async def run(c, params, ctx):
    prefix = ctx["prefix"]
    if c not in commands:
        r = f"Unknown command: `{prefix}{c}`"
        return False, r
    cmd = commands[c]

    if cmd.admin_required and not ctx["admin"]:
        return False, "Sorry. You don't have the required permissions for this command."
    
    if cmd.team_required and not (ctx['team'] or ctx['admin']):
        return False, "Sorry. You don't have the required permissions for this command."
    
    if len(params) < cmd.params_required:
        return False, f"Not enough parameters were given.\n{len(params)} parameters were given, {cmd.params_required} parameters were expected."

    try:
        r = await cmd.execute(ctx, params)
    except discord.errors.Forbidden:
        return False, "I don't have permission to do that."
    
    if r is None:
        return False, f"An unknown Error occured while ececuting command `{c}`"
    
    return r
