import os
import json
# from utils import get_config

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
SCRIPT_DIR = SCRIPT_DIR + ("/" if not SCRIPT_DIR.endswith("/") else "")


def read_json(fp):
    'return data from json'
    with open(fp, "r") as f:
        data = json.load(f)
    return data

def get_config():
    'import config.json'
    cf = os.path.join(SCRIPT_DIR + "config.json")
    if not os.path.exists(cf):
        print("Config doesn't exist!")
        import sys
        sys.exit()
    return read_json(cf)

CONFIG = get_config()

BOT_TEST_CHANNEL_ID = CONFIG["bot_test-channel"]


# "member" will be replaced by the mention-tag
JOIN_MSGS = [
    f"Welcome member! You can't leave now."
    f"Wrong Server member!",
    f"This is not the afterlife member!",
    f"member, Turn around!"
]

# "member" will be replaced by the mention tag
LEAVE_MSGS = [
    f"Ok, bye then, member..."
    f"You're a fish, member.",
    f"It was all a dream, member.",
    f"member, nothing is true.",
    f"member, I have nothing."
]