import discord

from commands.base import Cmd


async def execute(ctx, params):
    try:
        r = await ctx["channel"].send("One moment...")
    except discord.errors.Forbidden:
        return False, f"Can't send message in channel {ctx['channel'].name}."
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
    return True, "NO RESPONSE"



command = Cmd(
    execute=execute,
    help_text="",
    params_required=0,
    admin_required=False
)

