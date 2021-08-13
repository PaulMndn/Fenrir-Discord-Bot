import discord
import os
import json
import shelve
import logging

import cfg



def get_config():
    'import config.json'
    logging.info("Import config.json")
    cf = cfg.SCRIPT_DIR / "config.json"
    if not cf.exists():
        logging.critical("Config file does not exist! Programm will shut down.")
        import sys
        sys.exit()
    
    with open(cf, "r") as config:
        return json.load(config)


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


def ensure_guild_folder(guild):
    "Make sure guild data folder exists."
    dir = cfg.DATA_DIR / str(guild.id)
    if not dir.exists:
        dir.mkdir()


def get_default_settings():
    'get default settings from data/default.json'
    fp = str(cfg.DATA_DIR/"default_settings.json")
    with open(fp, "r") as default_settings:
        return json.load(default_settings)


def get_guild_settings(guild) -> dict:
    '''Get guild settings.
    
    Args:
        guild: guild object
    
    Returns:
        dict of guild settings
    '''
    guild_settings = get_default_settings()

    # add/overwrite with guild-specific settings
    with shelve.open(str(cfg.DATA_DIR/str(guild.id)/"settings")) as settings:
        for k,v in settings.items():
            guild_settings[k] = v
    
    return guild_settings


def reset_guild_settings(guild: discord.Guild):
    "Delete all guild specific settings"
    with shelve.open(str(cfg.DATA_DIR/str(guild.id)/"settings")) as settings:
        for i in settings:
            del settings[i]
    return True





if __name__ == "__main__":
    print(get_default_settings())