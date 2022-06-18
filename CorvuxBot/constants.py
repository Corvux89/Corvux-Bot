import os

# TODO: Make a lot of these loadable/outside constants

# BOT Config
TOKEN = os.environ['BOT_TOKEN']
COMMAND_PREFIX = os.environ['COMMAND_PREFIX']
DEBUG_GUILDS = [226741726943903754]
GAME_NAME = "Doom on Kindle Paperwhite"
GAME_TYPE = "gaming"


# Google Sheets
GOOGLE_SERVICE_ACCOUNT = os.environ['GOOGLE_KEY_JSON']
WORKBOOK_ID = os.environ['WORKBOOK_ID']

# Roles
MAGEWRITE_ROLE = [986009661377478699]

# Admin Stuff
ADMIN_USERS = [225752877316964352]  # Corvux
#ADMIN_USERS = [208388527401074688]  # Alesha
COGS_DIR = "CorvuxBot/cogs"
COGS_PATH = "CorvuxBot.cogs"

# Emotes
GREY_QUESTION = "<:grey_question:983576825294884924>"
WHITE_CHECK = "<:white_check_mark:983576747381518396>"
BOOKMARK = "<:bookmark:986735232604598302>"
RED_X = "<:x:983576786447245312>"
BAD_URL="https://tenor.com/view/nope-not-a-chance-no-gif-13843355"

# Dashboard stuff
MAGEWRITE_ROLE = [986009661377478699]
CHUNKS = 20
EXCLUDED_CHANNElS = {
    983857820803932230: [985880854154846220, 986749254292865076],
    987023548902154240: [987038594118074408]
}

AVAILABLE = f'{WHITE_CHECK} = Channel available\n'
WAITING = f'{BOOKMARK} = Waiting for Magewright\n'
BUSY = f'{RED_X} = Channel in use\n'