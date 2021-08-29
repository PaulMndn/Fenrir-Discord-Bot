# import os
import pathlib
import json
import utils

SCRIPT_DIR = pathlib.Path()
DATA_DIR = SCRIPT_DIR / "data"
# SCRIPT_DIR = SCRIPT_DIR + ("/" if not SCRIPT_DIR.endswith("/") else "")

CONFIG = utils.get_config()

BOT_TEST_CHANNEL_ID = CONFIG["bot_test-channel"]

PREFIX = "!"


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

LOADING_MSGS = [
    "......... Oh shit, you were waiting for me to do something? Oh okay, well then.",
    "Not panicking...totally not panicking...er...everything's fine...",
    "Following the white rabbit....",
    '"Going the distance..."',
    "The Elders of the Internet are contemplating your request...",
    "PC Load Letter!? What the $#%& does that mean?",
    "All your base are belong to us",
    "Baking cake...er...I mean loading, yeah loading...",
    "I'll be with you in a bit...(snicker)",
    "Let this abomination unto the Lord begin",
    "Making stuff up. Please wait...",
    "Searching for the... OMG, what the heck is THAT doing there?",
    "Loading the Loading message....",
    "The internet is full... Please wait...",
    "Checking prime directives: Serve the public trust...Protect the innocent...Uphold the law...Classified....",
    "Slackbot is groggy. installing java",
    "Initializing Skynet library. gaining sentience....",
    "I'm quite drunk, loading might take a little more time than the usual! Please be patient....",
    "Commencing infinite loop (this may take some time)....",
    "Caching internet locally....",
    "Water detected on drive C:, please wait. Spin dry commencing",
    "Yes there really are magic elves with an abacus working frantically in here",
    "Load failed. retrying with --prayer....",
    "Performing the rite of percussive maintenance....",
    "Sacrificing a resistor to the machine gods...."
]


# global volatile storage
availabilities = {}