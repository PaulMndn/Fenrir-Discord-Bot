import requests
import pandas as pd
import datetime as dt

def match_history():
    'Returns string of previous matches. Output in monospace characters recommended'
    
    url = r"https://vrmasterleague.com/EchoArena/Teams/I0s62s81gK1eswlVkTNz6Q2"
    r = requests.get(url)
    tables = pd.read_html(r.text)
    matches = tables[2]
    
    matches = matches.drop(columns=["VOD", "MATCH PAGE"])
    matches["DATE PLAYED"] = pd.to_datetime(matches["DATE PLAYED"]).dt.date
    clean_matches = matches.copy()
    clean_matches.columns = ["" for i in clean_matches]
    clean_matches.index = ["" for i in range(len(clean_matches))]

    return str(clean_matches)

