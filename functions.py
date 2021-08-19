from lib.event import Event
import discord
import requests
import pandas as pd
import datetime as dt
import shelve
import logging
import requests

import cfg
import utils



def match_history(home_team = "Fenrir"):        # TODO: better formatting of output
    'Returns string of previous matches. Output in monospace characters recommended'
    
    url = r"https://vrmasterleague.com/EchoArena/Teams/SRo_nCsh6RT2Py5X5_iUyw2"
    r = requests.get(url)
    tables = pd.read_html(r.text)
    matches = tables[-1]
    
    matches = matches.drop(columns=["VOD", "MATCH PAGE"])
    matches["DATE PLAYED"] = pd.to_datetime(matches["DATE PLAYED"]).dt.date

    lines = []
    match_dict = matches.to_dict()
    for i in range(len(matches)):
        row = [f"{match_dict['DATE PLAYED'][i]}:"]
        team_a = match_dict["ORANGE"][i]
        team_b = match_dict["BLUE"][i]
        scores = match_dict["SCORE"][i].split(" - ")
        if team_a == home_team:
            row.append(team_a)
            row.append(f"{scores[0].zfill(2)} - {scores[1].zfill(2)}")
            row.append(team_b)
        else:
            row.append(team_b)
            row.append(f"{scores[1].zfill(2)} - {scores[0].zfill(2)}")
            row.append(team_a)
        lines.append("  ".join(row))
    
    return "\n".join(lines)



# maybe move over to utils
def get_events(guild) -> list[Event]:
    'Returns list of event objects for this guild.'
    with shelve.open(str(cfg.DATA_DIR / str(guild.id) / "events")) as events:
        out = list(events.values())
        return out


# maybe move over to utils
def add_event(guild: discord.Guild, event:Event):
    with shelve.open(str(cfg.DATA_DIR / str(guild.id) / "events")) as events:
        events[event.key] = event
    return True


def rem_event(guild: discord.Guild, date: dt.datetime):
    '''Removes an event from the guilds planner.
    
    Args: 
        guild: planner of this guild will be edited
        date: datetime of event to identify it
    
    Returns: 
        (bool, str): True and removed event when success,
            False and "KeyError" if failed
    '''
    logging.debug(f"Removing event {date} from event db for guild {guild.name}, ID: {guild.id}.")
    with shelve.open(str(cfg.DATA_DIR / str(guild.id) / "events")) as events:
        try:
            event = next(e for e in events.values() if e.date_time == date)
            deleted_event = events.pop(event.key)
        except KeyError:
            logging.error(f"No event with {date} exists in the event planner.")
            return False, "KeyError"
    return True, event






if __name__ == "__main__":
    print(match_history())
    pass
