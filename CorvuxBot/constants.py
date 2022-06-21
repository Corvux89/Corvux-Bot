import os
# https://discord.com/api/oauth2/authorize?client_id=984169379535142935&permissions=544857390288&scope=applications.commands%20bot

# TODO: Make a lot of these loadable/outside constants; Need to change DB from GSheets to an actual DB for this;

# BOT Config
TOKEN = os.environ['BOT_TOKEN']
COGS_DIR = "CorvuxBot/cogs"
COGS_PATH = "CorvuxBot.cogs"
COMMAND_PREFIX = os.environ['COMMAND_PREFIX']  # Move to DB
DEBUG_GUILDS = [226741726943903754]
GAME_NAME = "Doom on Kindle Paperwhite"
GAME_TYPE = "gaming"

#Database:
DATABASE_URL = os.environ['DATABASE_URL']

# Google Sheets
GOOGLE_SERVICE_ACCOUNT = os.environ['GOOGLE_KEY_JSON']
WORKBOOK_ID = os.environ['WORKBOOK_ID']

# Admin Stuff - Move to DB
ADMIN_USERS = [225752877316964352, 208388527401074688]  # Corvux
# ADMIN_USERS = [208388527401074688]  # Alesha

# Emotes
GREY_QUESTION = "<:grey_question:983576825294884924>"
WHITE_CHECK = "<:white_check_mark:983576747381518396>"
BOOKMARK = "<:bookmark:986735232604598302>"
RED_X = "<:x:983576786447245312>"

# Dashboard stuff - Move role and exclusions to DB
MAGEWRITE_ROLE = [986032020952055818]

AVAILABLE = f'{WHITE_CHECK} = Channel available\n'
WAITING = f'{BOOKMARK} = Waiting for Magewright\n'
BUSY = f'{RED_X} = Channel in use\n'
