from commands.base import Cmd



help_text = f"""I give help on how you can use me.

If no parameter is given, I'll list all commands available to you.
If you want help on a specific command try `<PREFIX><COMMAND> <command>`.
"""

def get_general_help(ctx):
    from commands import commands
    text = ["I can help you with the following commands:"]
    for name, cmd in commands.items():
        if not (cmd.admin_required or cmd.team_required):
            text.append(f"`{ctx['prefix']}{name}`")
    
    if ctx["team"] or ctx["admin"]:
        text.append("\nTeam commands:")
        for name, cmd in commands.items():
            if cmd.team_required:
                text.append(f"`{ctx['prefix']}{name}`")
    
    if ctx["admin"]:
        text.append("\nAdmin commands:")
        for name, cmd in commands.items():
            if cmd.admin_required:
                text.append(f"`{ctx['prefix']}{name}`")
    
    text.append(f"\nIf you want more info on a specific command try `{ctx['prefix']}{ctx['command']} command_name`.")
    
    return "\n".join(text)


def get_specific_help(ctx, cmd_name):
    from commands import commands
    if cmd_name not in commands:
        return f"Unknown command: `{cmd_name}`"
    cmd = commands[cmd_name]
    if (cmd.admin_required and not ctx["admin"]) \
        or (cmd.team_required and not (ctx['team'] or ctx['admin'])):
        return f"Sorry, you don't have the necessary permissions to use the command `{ctx['prefix']}{cmd_name}`."
    help_text = cmd.help_text
    if not help_text:
        return f"There is currently no help available for the command {cmd_name}"
    else:
        return help_text.replace("<PREFIX>", ctx['prefix']).replace("<COMMAND>", cmd_name)


async def execute(ctx, params):
    if not params:
        return get_general_help(ctx)
    else:
        return get_specific_help(ctx, params[0])


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    team_required=False,
    admin_required=False
)
