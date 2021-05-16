import discord
# import commands
from . import (
    history,
    ping,
    planner_add,
    planner_remove,
    planner
)

commands = {
    "history": history.command,
    "ping": ping.command,
    # "planner_add": planner_add.command,
    # "planner_remove": planner_remove.command,
    # "planner": planner.command
}

async def run(c, params, ctx):
    prefix = ctx["prefix"]
    if c not in commands:
        r = f"Unknown command: `{prefix}{c}`"
        return False, r
    cmd = commands[c]

    if cmd.admin_required and not ctx["admin"]:
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
