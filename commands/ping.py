import discord
import logging
import utils
import functions

from commands.base import Cmd

log = logging.getLogger(__name__)


help_text = "Ping me to get the some usefull info about me, like reaction time, latency and server region."


async def execute(ctx, params):
    try:
        r = await ctx["channel"].send(utils.get_loading_msg())
    except discord.errors.Forbidden:
        log.error(f"Can't send message in channel {ctx['channel'].name}.")
        await functions.dm_user(user= ctx['message'].author, 
                                msg=f"Can't send message in channel {ctx['channel'].mention}.")
        
        return
    t1 = ctx["message"].created_at
    t2 = r.created_at
    rt = (t2-t1).total_seconds()
    e = '😭' if rt > 5 else ('😨' if rt > 1 else '👌')
    embed = discord.Embed()
    embed.add_field(name="Reaction time:", value=f"{rt:.3f}s {e}", inline=False)
    lt = ctx['client'].latency
    e = '😭' if lt > 5 else ('😨' if lt > 1 else '👌')
    embed.add_field(name="Discord latency:", value=f"{lt:.3f}s {e}", inline=False)
    guild = ctx["guild"]
    embed.add_field(name="Guild region:", value=guild.region, inline=False)
    
    await r.edit(content="Pong!", embed=embed)
    return



command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    team_required=False,
    admin_required=False
)

