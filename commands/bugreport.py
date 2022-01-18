import logging
import discord

from commands.base import Cmd
from functions import dm_admin
from lib.errors import CommandError

log = logging.getLogger(__name__)


help_text = """
Report a bug to the developer.
Please ensure to also include a way to reproduce a bug if possible.

You may also create an issue at <https://github.com/PaulMndn/Fenrir-Discord-bot/issues>.

USAGE:
```<PREFIX><COMMAND> bug-description```\
"""



async def execute(ctx, params):
    message = ctx['message']
    guild = ctx['guild']
    report = ctx['message'].content.split("bugreport",1)[1]
    if len(report > 4096):
        CommandError("Your bug description is too long. The maximum number of characters allowed is 4096.")
    embed = discord.Embed(title="Bugreport")
    embed.description = report
    embed.set_footer(text=f"From {message.author.name}#{message.author.discriminator} in {guild.name}")
    await dm_admin(ctx['client'], message="", embed=embed)


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=1,
    team_required=True,
    admin_required=False
)

