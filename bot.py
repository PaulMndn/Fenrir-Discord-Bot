import discord
import logging
import random

import utils
import cfg

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



