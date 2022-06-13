from discord.ext import commands
from CorvuxBot.sheets_client import GSheetsClient
from CorvuxBot.contants import *


def is_admin(ctx):
    return ctx.author.id in ADMIN_USERS


class CorvuxBot(commands.Bot):
    def __init__(self, **options):
        super(CorvuxBot, self).__init__(**options)
        self.sheets=GSheetsClient()

