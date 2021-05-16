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

def get_planner():
    pass

def save_planner():
    pass