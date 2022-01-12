import discord
import shelve
import logging

from discord import utils

from commands.base import Cmd
import cfg
from lib.errors import CommandError
import utils

log = logging.getLogger(__name__)


help_text = """Display and edit the bot settings for this server.

Display the settings by using `<PREFIX><COMMAND>`.
Modify a setting by adding the setting and value behind the command. Role or channel values need to be tagged (@Role, #channel).

Following settings exist:
```
team_name               The name of the team. This is used as default for the `history` command.
team_role               Role with permissions to team commands. @Role when modifying.
events_channel          Channel to post events in. Tag new channel when modifying. (Default: None)
send_event_message      Send event messages in events_channel. (Default: False)
event_creation_ping     Ping team_role when new event is created. Requires send_event_message to be True. (Default: False)
member_join_msg         Send message on member join in system channel. (Default: False)
member_leave_msg        Send message on member leave in system channel. (Default: False)
```\

USAGE: 
```<PREFIX><COMMAND> [setting] [new_value]```\

EXAMPLES:
```<PREFIX><COMMAND>
<PREFIX><COMMAND> team_name Fenrir```
""" #TODO: use member_join_msg, member_leave_msg, event_creation_ping, send_event_message


def set_team_role(ctx, new_val):
    setting = "team_role"
    guild = ctx['guild']
    settings = ctx['settings']

    try:
        id = int(new_val.strip("<>#@!&"))
    except ValueError:
        raise CommandError("Invalide role/ID. Please tag the channel or use the role ID.")
    role = guild.get_role(id)
    if role is None or not isinstance(role, discord.Role):
        log.error(f"Invalid role to set as team_role for guild {guild.name}, ID: {guild.id}")
        raise CommandError("Invalide role/ID. Please tag the channel or use the role ID.")

    old_val = settings[setting]
    settings[setting] = id
    return old_val


def set_team_name(ctx, new_val):
    setting = "team_name"
    old_val = ctx['settings'][setting]
    ctx['settings'][setting] = new_val
    return old_val


def set_events_channel(ctx, new_val):
    setting = "events_channel"
    guild = ctx['guild']
    settings = ctx['settings']

    try:
        id = int(new_val.strip("<>#@!&"))
    except ValueError:
        raise CommandError("Invalide channel/ID. Please tag the channel or use the channel ID.")
    channel = guild.get_channel(id)
    if channel is None or not isinstance(channel, discord.TextChannel):
        log.error(f"Invalid channel to set as events_channel for guild {guild.name}, ID: {guild.id}")
        raise CommandError("Invalide channel/ID. Please tag the channel or use the channel ID.")

    old_val = settings[setting]
    settings[setting] = id
    return old_val


def set_send_event_message(ctx, new_val):
    setting = "send_event_message"
    settings = ctx['settings']

    new_val = utils.text_to_bool(new_val)
    if new_val is None:
        raise CommandError(f"Only `True` and `False` are valid values for `{setting}`.")

    old_val = settings[setting]
    settings[setting] = new_val
    return old_val


def set_event_creation_ping(ctx, new_val):
    setting = "event_creation_ping"
    settings = ctx['settings']

    new_val = utils.text_to_bool(new_val)
    if new_val is None:
        raise CommandError(f"Only `True` and `False` are valid values for `{setting}`.")

    old_val = settings[setting]
    settings[setting] = new_val
    return old_val


def set_member_join_msg(ctx, new_val):
    setting = "member_join_msg"
    settings = ctx['settings']

    new_val = utils.text_to_bool(new_val)
    if new_val is None:
        raise CommandError(f"Only `True` and `False` are valid values for `{setting}`.")

    old_val = settings[setting]
    settings[setting] = new_val
    return old_val


def set_member_leave_msg(ctx, new_val):
    setting = "member_leave_msg"
    settings = ctx['settings']

    new_val = utils.text_to_bool(new_val)
    if new_val is None:
        raise CommandError(f"Only `True` and `False` are valid values for `{setting}`.")

    old_val = settings[setting]
    settings[setting] = new_val
    return old_val


setters = {
    "team_role":           set_team_role,
    "team_name":           set_team_name,
    "events_channel":      set_events_channel,
    "send_event_message":  set_send_event_message,
    "event_creation_ping": set_event_creation_ping,
    "member_join_msg":     set_member_join_msg,
    "member_leave_msg":    set_member_leave_msg
}


async def execute(ctx, params):
    log.info(f"Executing command {ctx['command']} {ctx['params_str']}.")
    guild:discord.Guild = ctx['guild']
    settings = ctx['settings']
    
    if len(params) == 0:
        # return current settings
        ret = f"Your current settings:\n```{settings}```"
        log.debug("Returning all settings with current values")
        return ret
    
    elif params[0] == "reset":
        if len(params) == 1:
            # reset to default settings
            old_settings_str = str(settings)
            settings.reset()
            return "Your settings have been reset to the default values.\n\n" \
                f"These were your settings before:\n```{old_settings_str}```"
        else:
            setting = params[1]
            if setting not in settings:
                raise CommandError(f"`{setting}` does not exist.")
            old_val = settings[setting]
            del settings[setting]
            return f"`{setting}` was reset from `{old_val}` to its default value `{settings[setting]}`."

    elif len(params) >= 2:
        # setting and new value included
        setting = params[0]
        new_val = " ".join(params[1:])

        try:
            s = setters[setting]
        except KeyError:
            raise CommandError(f"Setting `{setting}` does not exist.")
        
        old_val = s(ctx, new_val)       # FIXME: raises KeyError at least for `send_event_message` 
        
        return f"`{setting}` was changed from `{old_val}` to `{settings[setting]}`."

    else:
        # Invalid number of parameters
        raise CommandError("Invalid parameters. See help for more information.")
    



command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    team_required=False,
    admin_required=True
)
