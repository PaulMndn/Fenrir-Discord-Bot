import os
import json
import shelve

import cfg



def read_json(fp):
    'return data from json'
    with open(fp, "r") as f:
        data = json.load(f)
    return data

def get_config():
    'import config.json'
    cf = os.path.join(cfg.SCRIPT_DIR + "config.json")
    if not os.path.exists(cf):
        print("Config doesn't exist!")
        import sys
        sys.exit()
    return read_json(cf)


def write_db(guild, key, data):
    fp = os.path.join(cfg.SCRIPT_DIR, "data", "database")
    with shelve.open(fp, writeback=True) as db:
        if not str(guild.id) in db:
            db[str(guild.id)] = {}
        
        db[str(guild.id)][key] = data
    return True

def read_db(guild, key):
    fp = os.path.join(cfg.SCRIPT_DIR, "data", "database")
    with shelve.open(fp) as db:
        if not str(guild.id) in db:
            db[str(guild.id)] = {}
        try:
            data = db[str(guild.id)][key]
        except KeyError:
            ret = False
    if not ret:
        return False
    else:
        return data

def get_planner():
    pass

def save_planner():
    pass