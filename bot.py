import discord
import logging
import random

import cfg
import utils
import functions as func
import commands


logging.basicConfig(
    filename="bot.log", 
    encoding="utf-8", 
    level=logging.DEBUG, 
    format="%(asctime)s %(levelname)s - %(name)s: %(message)s",
    force=True
)
logging.info("""
#############################################
############     Starting...     ############
#############################################"""
)


intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.typing = False
intents.webhooks = False
intents.invites = False
intents.integrations = False

DEV_TOKEN = cfg.CONFIG["dev_token"]
TOKEN = cfg.CONFIG["token"]
# print(TOKEN)

client = discord.Client(intents = intents)


@client.event
async def on_ready():
    for g in client.guilds:
        utils.ensure_guild_folder(g)

    activity = discord.Activity(type=discord.ActivityType.listening, name = f"{cfg.PREFIX}help")
    await client.change_presence(activity=activity)
    logging.info(f"Logged in as {client.user}")

@client.event
async def on_guild_join(guild):
    utils.ensure_guild_folder(guild)
    

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
        await message.channel.send("Sorry, I currently don't react to DMs.")
        return

    prefix_p = cfg.PREFIX
    prefix = None
    if message.content.startswith(prefix_p):
        prefix = prefix_p
    
    if prefix:
        logging.debug(f"Recieved message {message.content}"
            + f" in channel {message.channel.name}"
            + f" of guild {message.guild.name}"
        )
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
            "prefix": prefix,
            "team": False,
            "admin": False
        }

        team_role_id = utils.get_guild_settings(guild)["team_role"]
        if team_role_id is not None:
            if team_role_id in [role.id for role in message.author.roles]:
                ctx["team"] = True
        print(ctx['team'])
            
        if message.author.permissions_in(channel).administrator:
            ctx["admin"] = True

        success, response = await commands.run(cmd, params, ctx)

        if success:
            logging.debug(f"Successfully executed command {ctx['command']}. Response: {response}")
        
        if success and response != "NO RESPONSE":
            await message.channel.send(response)
            return True
        
        if not success:
            if response != "NO RESPONSE":
                await message.channel.send(f":no_entry_sign: **An error occured.** :no_entry_sign:\n{response}")
                logging.error(f"Command: {message.content} Response: {response}")
                return False
            else:
                await message.channel.send("**An unnown error occured.**")
                logging.error(f"Unknown error while executing the command: {message.content}")
                return False
        


@client.event
async def on_member_join(member):
    # if member.guild.id not in cfg.VALID_SERVERS:
    #     return
    msg = random.choice(cfg.JOIN_MSGS).replace("MEMBER", member.mention)
    await member.guild.system_channel.send(msg)

@client.event
async def on_member_remove(member):
    # if member.guild.id not in cfg.VALID_SERVERS:
    #     return
    msg = random.choice(cfg.LEAVE_MSGS).replace("MEMBER", f"{member.name}#{member.discrimator}")
    await member.guild.system_channel.send(msg)



@client.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    funcs = utils.get_react_msg_funcs(reaction.message.guild, reaction.message)
    if funcs is False:
        return
    
    # execute add function
    await funcs[0](reaction, user)


@client.event
async def on_reaction_remove(reaction, user):
    if user.bot:
        return
    funcs = utils.get_react_msg_funcs(reaction.message.guild, reaction.message)
    if funcs is False:
        return
    
    # execute remove function
    await funcs[1](reaction, user)





client.run(DEV_TOKEN)



