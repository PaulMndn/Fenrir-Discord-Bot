#! /usr/bin/python3

import discord
import logging
from logging.handlers import RotatingFileHandler
import random
import traceback

import cfg
from lib.errors import CommandError
import lib.settings
import utils
import functions as func
import commands


logging.getLogger("discord").setLevel(logging.WARNING)


IS_DEV = cfg.CONFIG['is_dev']

LOG_FILE = "log/bot.log"
formatter = logging.Formatter("%(asctime)s %(levelname)s - %(name)s: %(message)s")
handler = RotatingFileHandler(
    filename=LOG_FILE,
    mode="a",
    maxBytes=5*1024*1024, # 5 MiB
    backupCount=5,
    encoding="utf-8"
)
handler.setFormatter(formatter)
log = logging.getLogger()
log.setLevel(logging.INFO if not IS_DEV else logging.DEBUG)
log.addHandler(handler)


log.info("""
#############################################
############     Starting...     ############
#############################################"""
)
if IS_DEV:
    log.info("Launching in Dev-Mode.")


intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.typing = False
intents.webhooks = False
intents.invites = False
intents.integrations = False

if IS_DEV:
    try:
        TOKEN = cfg.CONFIG["dev_token"]
    except KeyError:
        log.fatal("Application is running in dev-mode but no dev token is available in config.json.")
else:
    TOKEN = cfg.CONFIG["token"]

client = discord.Client(intents = intents)


@client.event
async def on_ready():
    for g in client.guilds:
        utils.ensure_guild_folder(g)

    activity = discord.Activity(type=discord.ActivityType.listening, name = f"{cfg.PREFIX}help")
    await client.change_presence(activity=activity)
    log.info(f"Logged in as {client.user}")

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
    
    if not message.guild: # DM
        if not message.author.id == cfg.CONFIG['admin_id']:
            await message.channel.send("Sorry, I currently don't react to DMs.")
            return

        text = message.content.strip()
        if text.startswith("log"):
            line_count = 25

            params = text.split()[1:]
            if params:
                try:
                    line_count = int(params[0])
                except ValueError:
                    pass

            replacement_emojis = {
                "DEBUG": "🚧",
                "INFO": "🗒️",
                "WARNING": "⚠️",
                "ERROR": "‼️",
                "CRITICAL": "💀",
                "FATAL": "💀"
            }

            with open(LOG_FILE, "r", encoding="utf-8") as lf:
                lines = lf.readlines()[-line_count:]
                for line in lines:
                    for k,v in replacement_emojis.items():
                        line = line.replace(k,v)
                    if len(line) > 2000:
                        line = line[-2000:]
                    line = f"{line}"
                    await func.dm_admin(client, line)


    if IS_DEV and not message.guild.id == cfg.TEST_GUILD_ID:
        # only react to messges in test-guild
        # for testing purposes
        return


    prefix_p = cfg.PREFIX
    prefix = None
    if message.content.startswith(prefix_p):
        prefix = prefix_p
    
    if prefix:
        # message has prefix, so meant for bot
        log.info(f"Recieved message from {message.author.name}#{message.author.discriminator} {message.author.id}: "
            + f"{message.content}    "
            + f"Guild: {message.guild.name}, {message.guild.id}, "
            + f"Channel: {message.channel.name}, {message.channel.id}"
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
            "settings": lib.settings.GuildSettings(guild),
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
            
        if message.author.permissions_in(channel).administrator:
            ctx["admin"] = True

        try:
            log.debug("Start executing command.")
            response = await commands.run(cmd, params, ctx)
            if response is not None:
                await channel.send(response)
            log.info(f"Successfully executed command. Response: {repr(response)}")
        except CommandError as e:
            await channel.send(f"An error occured.\n{e}")
            log.error(f"Command: {message.content} Response: {e}")
        except Exception as e:
            log.error(f"An error occured when executing the command {message.content}: \n{traceback.format_exc()}")
            await message.channel.send("An unknown error occured.")
            raise



@client.event
async def on_message_delete(message):
    func.rem_event_from_msg(message)
    


@client.event
async def on_member_join(member):
    # if member.guild.id not in cfg.VALID_SERVERS:
    #     return
    log.debug(f"Member {member.name}#{member.discriminator} joined server {member.guild.name} {member.guild.id}.")
    msg = random.choice(cfg.JOIN_MSGS).replace("MEMBER", member.mention)
    await member.guild.system_channel.send(msg)

@client.event
async def on_member_remove(member):
    # if member.guild.id not in cfg.VALID_SERVERS:
    #     return
    log.debug(f"Member {member.name}#{member.discriminator} left server {member.guild.name} {member.guild.id}.")
    msg = random.choice(cfg.LEAVE_MSGS).replace("MEMBER", f"{member.name}#{member.discrimator}")
    await member.guild.system_channel.send(msg)



@client.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    funcs = utils.get_react_msg_funcs(reaction.message.guild, reaction.message)
    if funcs is False:
        return
    
    log.info(f"Reaction {reaction.emoji} was added to message {reaction.message.id} by user {user.name}#{user.discriminator} {user.id}.")
    # execute add function
    await funcs[0](reaction, user)


@client.event
async def on_reaction_remove(reaction, user):
    if user.bot:
        return
    funcs = utils.get_react_msg_funcs(reaction.message.guild, reaction.message)
    if funcs is False:
        return
    
    log.info(f"Reaction {reaction.emoji} was removed from message {reaction.message.id} by user {user.name}#{user.discriminator} {user.id}.")
    # execute remove function
    await funcs[1](reaction, user)





client.run(TOKEN)



