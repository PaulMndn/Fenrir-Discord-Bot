import discord
import shelve
import logging

from commands.base import Cmd
import cfg
from utils import get_guild_settings, reset_guild_settings

help_text = """Display and edit the bot settings for this server.

Display the settings by using `<PREFIX><COMMAND>`.
Modify a setting by adding the setting and value behind the command. Role or channel values need to be tagged (@Role, #channel).

Following settings exist:
```
events_channel       Channel to post events in. Tag new channel when modifying.
team_role           Role with permissions to team commands. @Role when modifying.
```

USAGE: `<PREFIX><COMMAND> [setting new_value]`

EXAMPLES:
```
<PREFIX><COMMAND>
```
"""


async def execute(ctx, params):
    logging.info(f"Executing command {ctx['command']} {ctx['params_str']}.")
    guild:discord.Guild = ctx['guild']
    
    if len(params) == 0:
        # no further parameters, return all current values
        settings = get_guild_settings(guild)
        ret = "Your current settings:\n```\n" + "\n".join(f"{s:<20}{v}" for s,v in settings.items()) + "\n```"
        logging.debug("Returning all settings with current values")
        return True, ret
    
    elif len(params) == 1 and params[0] == "reset":
        old_settings = get_guild_settings(guild)
        old_settings = "\n".join(f"{k:<20}{v}" for k,v in old_settings.items())
        reset_guild_settings(guild)
        return True, "Your settings have been reset to the default values.\n\n" \
            f"These were your settings before:\n```\n{old_settings}\n```"

    elif len(params) == 2:
        # setting and new value included
        setting = params[0]
        new_val = params[1]
        guild_settings = get_guild_settings(guild)
        
        if setting not in guild_settings:
            return False, f"Setting {setting} does not exist."

        # check validity of new value
        id = int(new_val.strip("<>#@!&"))
        if setting == "events_channel" and guild.get_channel(id) is None:
            logging.error(f"Invalid channel to set as events_channel for guild {guild.name}, ID: {guild.id}")
            return False, "Invalide channel"
        elif setting == "team_role" and guild.get_role(id) is None:
            logging.error(f"Invalid role to set as team_role for guild {guild.name}, ID: {guild.id}")
            return False, "Invalide Channel"
        
        # update settings
        old_val = guild_settings[setting]
        with shelve.open(str(cfg.DATA_DIR / str(guild.id) / "settings")) as settings:   # outsource to utils?
            settings[setting] = id
            logging.info(f"Changed setting {setting} from {old_val} to {id} for server {ctx['guild'].name}, ID: {ctx['guild'].id}.")
        
        return True, f"{setting} was changed from {old_val} to {new_val}."

    else:
        # Invalid number of parameters
        return False, "Invalid parameters. See help for more information."
    




command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    team_required=False,
    admin_required=True
)
