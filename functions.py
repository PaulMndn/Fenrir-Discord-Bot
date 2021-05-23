import discord
import requests
import pandas as pd
import datetime as dt
import shelve
import os

import cfg
import utils


def match_history(home_team = "Fenrir"):        # TODO: better formatting of output
    'Returns string of previous matches. Output in monospace characters recommended'
    
    url = r"https://vrmasterleague.com/EchoArena/Teams/I0s62s81gK1eswlVkTNz6Q2"
    r = requests.get(url)
    tables = pd.read_html(r.text)
    matches = tables[2]
    
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

    return str(clean_matches)


# maybe move over to utils
def get_events(guild):
    'Return dict of events for guild'
    with shelve.open(os.path.join(cfg.SCRIPT_DIR, "data", "database")) as db:
        if not str(guild.id) in db:
            db[str(guild.id)] = {}
        try:
            events = db[str(guild.id)]["events"]
        except KeyError:
            events = {}
    return events

# maybe move over to utils
def add_event(guild, date, name):
    with shelve.open(os.path.join(cfg.SCRIPT_DIR, "data", "database"), writeback=True) as db:
        if not str(guild.id) in db:
            db[str(guild.id)] = {}
        if not "events" in db[str(guild.id)]:
            db[str(guild.id)]["events"] = {date: name}
        
        db[str(guild.id)]["events"][date] = name
    
    return True


if __name__ == "__main__":
    # print(match_history("Team Gravity"))
    pass
