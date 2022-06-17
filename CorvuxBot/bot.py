from discord.ext import commands
from CorvuxBot.constants import ADMIN_USERS
from CorvuxBot.models.characters import *
from CorvuxBot.models.dashboard import *
from CorvuxBot.sheets_client import GSheetsClient


def is_admin(ctx):
    return ctx.author.id in ADMIN_USERS


class CorvuxBot(commands.Bot):
    sheets: GSheetsClient
    characters: characters
    dashboards: dashboards

    def __init__(self, **options):
        super(CorvuxBot, self).__init__(**options)
        self.characters = characters()
        self.dashboards = dashboards()
        self.sheet = GSheetsClient()