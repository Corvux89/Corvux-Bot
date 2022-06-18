import os

# TODO: Make a lot of these loadable/outside constants; Need to change DB from GSheets to an actual DB for this;

# BOT Config
TOKEN = os.environ['BOT_TOKEN']
COGS_DIR = "CorvuxBot/cogs"
COGS_PATH = "CorvuxBot.cogs"
COMMAND_PREFIX = os.environ['COMMAND_PREFIX']  # Move to DB
DEBUG_GUILDS = [226741726943903754]
#Move the following to a command structure and os.environ?...avtivity?
GAME_NAME = "Doom on Kindle Paperwhite"
GAME_TYPE = "gaming"


# Google Sheets
GOOGLE_SERVICE_ACCOUNT = os.environ['GOOGLE_KEY_JSON']
WORKBOOK_ID = os.environ['WORKBOOK_ID']

# Admin Stuff - Move to DB
ADMIN_USERS = [225752877316964352]  # Corvux
# ADMIN_USERS = [208388527401074688]  # Alesh

# Emotes
GREY_QUESTION = "<:grey_question:983576825294884924>"
WHITE_CHECK = "<:white_check_mark:983576747381518396>"
BOOKMARK = "<:bookmark:986735232604598302>"
RED_X = "<:x:983576786447245312>"

# Dashboard stuff - Move role and exclusions to DB
MAGEWRITE_ROLE = [986009661377478699]
EXCLUDED_CHANNElS = {
    983857820803932230: [985880854154846220, 986749254292865076],
    987023548902154240: [987038594118074408]
}
AVAILABLE = f'{WHITE_CHECK} = Channel available\n'
WAITING = f'{BOOKMARK} = Waiting for Magewright\n'
BUSY = f'{RED_X} = Channel in use\n'
