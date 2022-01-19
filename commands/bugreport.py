import logging
import discord

from commands.base import Cmd
from functions import dm_admin
from lib.errors import CommandError

log = logging.getLogger(__name__)


help_text = """
Report a bug to the developer.
Please ensure to also include a way to reproduce a bug if possible.

Bugs/issues can be reportet at <https://github.com/PaulMndn/Fenrir-Discord-bot/issues>.

You can also report a bug using this command. However, this is *not* preferred

USAGE:
```<PREFIX><COMMAND> [bug-description]```\
"""



async def execute(ctx, params):
    if not params:
        return "You may report bugs or make feature requests at <https://github.com/PaulMndn/Fenrir-Discord-bot/issues>."
    
    message = ctx['message']
    guild = ctx['guild']
    report = ctx['message'].content.split("bugreport",1)[1]
    if len(report) > 4096:
        CommandError("Your bug description is too long. The maximum number of characters allowed is 4096.")
    embed = discord.Embed(title="Bugreport")
    embed.description = report
    embed.set_footer(text=f"From {message.author.name}#{message.author.discriminator} in {guild.name}")
    await dm_admin(ctx['client'], message="", embed=embed)
    return "Your message has been sent to the developer.\n\n Note that it is preferred if you create an issue at <https://github.com/PaulMndn/Fenrir-Discord-bot/issues>."


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    team_required=True,
    admin_required=False
)

