import discord
from commands.base import Cmd

help_text = "Get an invite link to invite me to your server."

async def execute(ctx, params):
    inv_url = "https://discord.com/api/oauth2/authorize?client_id=846841732905828352&permissions=1236951100480&scope=bot"

    e = discord.Embed(
        title="Invite me!", 
        description=f'Glad you like me!\nInvite me to your server [**here**]({inv_url} "Bot invite link").')
    
    await ctx['channel'].send(content="", embed=e)



command = Cmd(
    execute=execute,
    help_text=help_text
)