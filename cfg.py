import os
import json
import utils

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
SCRIPT_DIR = SCRIPT_DIR + ("/" if not SCRIPT_DIR.endswith("/") else "")



CONFIG = utils.get_config()

BOT_TEST_CHANNEL_ID = CONFIG["bot_test-channel"]

PREFIX = "$"


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

# PLANNER = load_planner()