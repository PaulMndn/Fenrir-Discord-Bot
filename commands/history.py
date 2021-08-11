import discord
from functions import match_history

from commands.base import Cmd


help_text = "History of matches of team Fenrir."


async def execute(ctx, params):
    r = await ctx["channel"].send("Checking VRML.com...")

    embed = discord.Embed(
        title = "Match history", 
        # colour=0xffff00
    )
    embed.set_author(
        name="Fenrir", 
        url="https://vrmasterleague.com/EchoArena/Teams/SRo_nCsh6RT2Py5X5_iUyw2",
        icon_url="https://vrmasterleague.com/images/div_bronze_2_40.png"
    )
    embed.set_thumbnail(url="https://vrmasterleague.com/images/logos/teams/3d5c9260-0f0d-4b1a-a2b3-45ad7e9f9313.png")
    embed.set_footer(text=match_history())
    await r.edit(content="", embed=embed)
    
    return True, "NO RESPONSE"



command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    admin_required=False
)