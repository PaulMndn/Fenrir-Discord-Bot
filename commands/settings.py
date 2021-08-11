import shelve
import logging

from commands.base import Cmd
import cfg

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
    guild = ctx['guild']
    
    if len(params) == 0:
        # no further parameters, return all current values
        with shelve.open(str(cfg.DATA_DIR / str(guild.id) / "settings.json")) as settings:
            ret = "```\n" + "\n".join(f"{s<20}{v}" for s,v in settings.items()) + "\n```"
            logging.debug("Returning all settings with current values")
            return True, ret

    elif len(params) == 2:
        # setting and new value included
        setting = params[0]
        new_val = params[1]
        with shelve.open(str(cfg.DATA_DIR / str(guild.id) / "settings.json")) as settings:
            if setting not in settings:
                return False, f"Setting {setting} does not exist."
            old_val = settings[setting]
            settings[setting] = new_val
            logging.info(f"Changed setting {setting} from {old_val} to {new_val} for server {ctx['guild'].name}, ID: {ctx['guild'].id}.")
            return True, f"{setting} was changed from {old_val} to {new_val}."

    else:
        # Invalid number of parameters
        return False, "2 Parameters required to modify a setting: the setting and the new value."
    
