import discord
import logging
import random

import utils
import cfg
import functions as func

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.typing = False
intents.webhooks = False
intents.invites = False
intents.integrations = False

TOKEN = cfg.CONFIG["token"]
# print(TOKEN)

client = discord.Client(intents = intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    
    if not message.channel.id == cfg.BOT_TEST_CHANNEL_ID:
        return

    if message.content.startswith("!ping"):
        await message.channel.send(f"{message.author.mention} pong")

    if message.content.strip() == "!history":
        r = await message.channel.send("Checking VRML.com...")

        embed = discord.Embed(
            title = "Match history", 
            # description = func.match_history(), 
            colour=0xffff00
        )
        embed.set_author(
            name="Team Gravity", 
            url="https://vrmasterleague.com/EchoArena/Teams/I0s62s81gK1eswlVkTNz6Q2",
            icon_url="https://vrmasterleague.com/images/div_master_40.png"
        )
        embed.set_thumbnail(url="https://vrmasterleague.com/images/logos/teams/1259745d-c70e-4064-8907-1ee78fcc5725.png")
        embed.set_footer(text=func.match_history())
        await r.edit(content="For now Team Gravity's History streight from <VRML.com>", embed=embed)

@client.event
async def on_member_join(member):
    # if member.guild.id not in cfg.VALID_SERVERS:
    #     return
    msg = random.choice(cfg.JOIN_MSGS).replace("member", member.mention)
    await member.guild.system_channel.send(msg)

@client.event
async def on_member_remove(member):
    # if member.guild.id not in cfg.VALID_SERVERS:
    #     return
    msg = random.choice(cfg.LEAVE_MSGS).replace("member", member.mention)
    await member.guild.system_channel.send(msg)




client.run(TOKEN)



