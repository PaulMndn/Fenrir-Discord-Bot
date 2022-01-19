import discord

from lib.errors import CommandError
# import commands
from . import (
    availability,
    bugreport,
    event_add,
    event_remove,
    events,
    help,
    history,
    invite,
    ping,
    potato,
    settings,
)



commands = {
    "availability": availability.command,
    "bugreport": bugreport.command,
    "add-event": event_add.command,
    "events": events.command,
    "help": help.command,
    "history": history.command,
    "invite":invite.command,
    "ping": ping.command,
    "potato": potato.command,
    "remove-event": event_remove.command,
    "settings": settings.command
}

async def run(c, params, ctx):
    if c not in commands:
        return
    cmd = commands[c]

    if cmd.admin_required and not ctx["admin"]:
        raise CommandError("Sorry. You don't have the required permissions for this command.")
    
    if cmd.team_required and not (ctx['team'] or ctx['admin']):
        raise CommandError("Sorry. You don't have the required permissions for this command.")
    
    if len(params) < cmd.params_required:
        raise CommandError(f"Not enough parameters were given.\n{len(params)} parameters were given, {cmd.params_required} parameters were expected.")

    try:
        resp = await cmd.execute(ctx, params)
    except discord.errors.Forbidden:
        return False, "I don't have permission to do that."
    
    return resp
