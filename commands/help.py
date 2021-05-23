from typing import ContextManager
from commands.base import Cmd



help_text = f"""I give help on how you can use me.

If no parameter is given, I'll list all commands available to you.
If you want help on a specific command try `<PREFIX><COMMAND> <command>`.
"""


async def execute(ctx, params):
    if params == []:
        from commands import commands
        text = ["I can help you with the following commands:"]
        for c in commands:
            cmd = commands[c]
            if not cmd.admin_required:
                text.append(f"`{ctx['prefix']}{c}`")
        
        if ctx["admin"]:
            text.append("\nAdmin commands:")
            for c in commands:
                cmd = commands[c]
                if cmd.admin_required:
                    text.append(f"`{ctx['prefix']}{c}`")
        text.append(f"\nIf you want more info on a specific command try `{ctx['prefix']}{ctx['command']} <command>`.")

        return True, "\n".join(text)
    else:
        from commands import commands
        if params[0] not in commands:
            return False, f"Unknown command: `{params[0]}`"
        cmd = commands[params[0]]
        if cmd.admin_required and not ctx["admin"]:
            return True, f"Sorry, you don't have the necessary permissions to use the command `{ctx['prefix']}{params[0]}`."
        help_text = cmd.help_text
        if not help_text:
            return True, f"There is currently no help available for the command {params[0]}"
        else:
            return True, help_text.replace("<PREFIX>", ctx['prefix']).replace("<COMMAND>", params[0])



command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    admin_required=False
)
