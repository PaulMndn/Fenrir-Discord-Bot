# import os
import pathlib
import json
import utils

SCRIPT_DIR = pathlib.Path()
DATA_DIR = SCRIPT_DIR / "data"
# SCRIPT_DIR = SCRIPT_DIR + ("/" if not SCRIPT_DIR.endswith("/") else "")

CONFIG = utils.get_config()

BOT_TEST_CHANNEL_ID = CONFIG["bot_test-channel"]

PREFIX = "$"


# "MEMBER" will be replaced by the mention-tag
JOIN_MSGS = [
    "Welcome MEMBER! You can't leave now.",
    "Wrong Server MEMBER!",
    "This is not the afterlife MEMBER!",
    "MEMBER, Turn around!"
]

# "MEMBER" will be replaced by name#discriminator
LEAVE_MSGS = [
    "Ok, bye then, MEMBER...",
    "You're a fish, MEMBER.",
    "It was all a dream, MEMBER.",
    "MEMBER, nothing is true.",
    "MEMBER, I have nothing."
]

