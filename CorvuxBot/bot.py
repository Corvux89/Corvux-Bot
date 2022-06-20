import logging
from discord.ext import commands
from CorvuxBot.sheets_client import GSheetsClient

log = logging.getLogger(__name__)


class CorvuxBot(commands.Bot):
    sheets: GSheetsClient

    def __init__(self, **options):
        super(CorvuxBot, self).__init__(**options)
        self.sheet = GSheetsClient()



