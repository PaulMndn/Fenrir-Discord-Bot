import discord
from functions import match_history

from commands.base import Cmd


help_text = "History of matches of team Fenrir."


async def execute(ctx, params):
    r = await ctx["channel"].send("Checking VRML.com...")

    embed = discord.Embed(
        title = "Match history", 
        colour=0xffff00,
        description=f"```{match_history(home_team='Team Gravity')}``` "
    )
    embed.set_author(
        name="Team Gravity", 
        url="https://vrmasterleague.com/EchoArena/Teams/I0s62s81gK1eswlVkTNz6Q2",
        icon_url="https://vrmasterleague.com/images/div_master_40.png"
    )
    embed.set_thumbnail(url="https://vrmasterleague.com/images/logos/teams/1259745d-c70e-4064-8907-1ee78fcc5725.png")
    embed.set_footer(text=match_history(home_team="Team Gravity"))
    await r.edit(content="For now Team Gravity's history streight from <VRML.com>", embed=embed)
    
    return True, "NO RESPONSE"



command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    admin_required=False
)