import discord
import logging
import random

import utils
import cfg
import functions as func
import commands

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
    if not client.is_ready():
        return

    if message.author.bot:
        # Don't react to bots
        return
    
    if not message.channel.id == cfg.BOT_TEST_CHANNEL_ID:
        # only react to messges in BOT_TEST_CHANNEL
        # for testing purposes
        return

    if not message.guild: # DM
        await message.channel.send("Sorrs, I currently don't react to DMs")
        return

    prefix_p = cfg.PREFIX
    prefix = None
    if message.content.startswith(prefix_p):
        prefix = prefix_p
    
    if prefix:
        msg = message.content[len(prefix):].strip()
        split = msg.split()
        cmd = split[0]
        params = split[1:]
        params_str = " ".join(params)

        guild = message.guild
        channel = message.channel

        ctx = {
            "client": client,
            "guild": guild,
            "channel": channel,
            "command": cmd,
            "message": message,
            "params_str": params_str,
            "prefix": prefix
        }

        success, response = await commands.run(cmd, params, ctx)

        if success and response != "NO RESPONSE":
            await message.channel.send(response)
            return True
        
        if not success:
            if response != "NO RESPONSE":
                await message.channel.send(f"An error occured.\n{response}")
                return False
            else:
                await message.channel.send("An unnown error occured.")
                return False
        


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



