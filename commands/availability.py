from typing import Tuple
import discord
import logging
from lib.errors import CommandError

import utils
import cfg
from commands.base import Cmd

log = logging.getLogger(__name__)

help_text = """I can keep track of availabilities for you. This is usefull for \
finding available dates for scsrims and matches.
Use no parameters to get the availabilities for the last querry.
Use one or two parametes to define the span of days you want to know the \
availability for. The second parameter, if given, must be greater or equal \
than the first.
Weekdays are identified by numbers: 1-Monday to 7-Sunday.

Usage:
```<PREFIX><COMMAND> [day_or_start_day] [end_day]```\

Examples:
```<PREFIX><COMMAND>
<PREFIX><COMMAND> 3
<PREFIX><COMMAND> 2 7```
"""

number_emoji = {
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣",
    6: "6️⃣", 
    7: "7️⃣"
}
emoji_number = {
    "1️⃣": 1,
    "2️⃣": 2,
    "3️⃣": 3,
    "4️⃣": 4,
    "5️⃣": 5,
    "6️⃣": 6,
    "7️⃣": 7
}
number_weekday = {
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday",
    7: "Sunday"
}


class Availability:
    def __init__(self, init_msg, yes_msg, no_msg, days:Tuple):
        self.init_msg = init_msg
        self.yes_msg = yes_msg
        self.no_msg = no_msg
        self.yes = {}
        self.no = {}
        for d in range(days[0], days[1]+1):
            self.yes[d] = []
            self.no[d] = []
        
    def yes_add(self, day:int, member):
        if day in self.yes:
            self.yes[day].append(member)
            return True
        else:
            return False

    def yes_rem(self, day:int, member):
        try:
            self.yes[day].pop(self.yes[day].index(member))
        except ValueError:
            pass

    def no_add(self, day:int, member):
        if day in self.no:
            self.no[day].append(member)
            return True
        else:
            return False

    def no_rem(self, day:int, member):
        try:
            self.no[day].pop(self.no[day].index(member))
        except ValueError:
            pass


async def yes_reaction_add(reaction, user):
    guild = reaction.message.guild
    a:Availability = cfg.availabilities[guild.id]
    if reaction.message.id == a.yes_msg.id:
        try:
            day = emoji_number[reaction.emoji]
        except KeyError:
            # reaction is not 1-7, so it's removed
            await reaction.clear()
            log.info(f"Reaction {reaction.emoji} is invalid and was removed.")
            return

        if not a.yes_add(day, user):
            # invalid reaction number for the query (eg. reaction 3 when querried for 4-7)
            await reaction.clear()
            log.info(f"Reaction {reaction.emoji} is invalid and was removed.")
    
async def yes_reaction_remove(reaction, user):
    guild = reaction.message.guild
    a = cfg.availabilities[guild.id]
    if reaction.message.id == a.yes_msg.id:
        day = emoji_number[reaction.emoji]
        a.yes_rem(day, user)
    
async def no_reaction_add(reaction, user):
    guild = reaction.message.guild
    a = cfg.availabilities[guild.id]
    if reaction.message.id == a.no_msg.id:
        try:
            day = emoji_number[reaction.emoji]
        except KeyError:
            # reaction is not 1-7, so it's removed
            await reaction.clear()
            log.info(f"Reaction {reaction.emoji} is invalid and was removed.")
            return
        
        if not a.no_add(day, user):
            # invalid reaction number for the query (eg. reaction 3 when querried for 4-7)
            await reaction.clear()
            log.info(f"Reaction {reaction.emoji} is invalid and was removed.")
    
async def no_reaction_remove(reaction, user):
    guild = reaction.message.guild
    a = cfg.availabilities[guild.id]
    if reaction.message.id == a.no_msg.id:
        day = emoji_number[reaction.emoji]
        a.no_rem(day, user)





async def send_availabilities(guild, channel):
    try:
        a = cfg.availabilities[guild.id]
    except KeyError:
        return "No availabilities stored yet."
    # return True, f"{a.yes}\n{a.no}" # temporary
    embed = discord.Embed(title = "Availabilities", url=a.init_msg.jump_url)
    for day in a.yes.keys():
        value = "\n".join(
                [f"✅ {u.name}" for u in a.yes[day]]
                + [f"❌ {u.name}" for u in a.no[day]]
            )
        embed.add_field(
            name=number_weekday[day], 
            value = value if value != "" else "No replies"
        )
    embed.set_footer(text = f"Query from {a.yes_msg.created_at.date()}")
    ref = a.init_msg if channel == a.init_msg.channel else None
    await channel.send(embed=embed, reference=ref)



def parse_params(params):
    '''Parse parameters and check if they are valide.

    Args:
        params (`list`): list of given parameters as string

    Retruns:
        `(True, Tuple)` if success. `Tuple` of start_day and end_day.

        `(False, string)` otherwise. Error message in `string`.'''
    from_day = params[0]
    to_day = params[1] if len(params) > 1 else from_day
    
    try:
        # parse input
        from_day = int(from_day)
        to_day = int(to_day)
        if not (from_day in range(1,8) and to_day in range(1,8)):
            raise ValueError
    except ValueError:
        raise CommandError("Parameter(s) must be an integer from 1 to 7.")

    if not to_day >= from_day:
        raise CommandError("Second parameter must be greater or equal to the first one")
    
    return from_day, to_day


async def ask_availabilities(params, guild, channel):
    from_day, to_day = parse_params(params)
    
    msg = await channel.send("React below on which days you can or can't play on. 1-Monday ... 7-Sunday")
    msg_yes = await channel.send("I can play on...")
    msg_no = await channel.send("I can **not** play on...")
    for day in range(from_day, to_day+1):
        await msg_yes.add_reaction(number_emoji[day])
        await msg_no.add_reaction(number_emoji[day])
    
    availability = Availability(msg, msg_yes, msg_no, (from_day,to_day))
    cfg.availabilities[guild.id] = availability
    log.debug("Availability object stored in variable (volatile).")

        
    utils.add_react_msg(guild, msg_yes, yes_reaction_add, yes_reaction_remove)
    utils.add_react_msg(guild, msg_no, no_reaction_add, no_reaction_remove)
    log.debug("Both messages added to shelve to keep track of messages that we want to listen to reactions on.")

    return 





async def execute(ctx, params):
    guild = ctx['guild']
    channel = ctx['channel']

    if len(params) == 0:
        return await send_availabilities(guild, channel)
    else:
        return await ask_availabilities(params, guild, channel)





command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    team_required=True,
    admin_required=False
)
