from discord.ext import commands
from CorvuxBot.models.characters import *
from CorvuxBot.contants import *
from CorvuxBot.models.dashboard import *


def is_admin(ctx):
    return ctx.author.id in ADMIN_USERS


class CorvuxBot(commands.Bot):
    characters: characters
    dashboards: dashboards

    def __init__(self, **options):
        super(CorvuxBot, self).__init__(**options)
        self.characters = characters()
        self.dashboards = dashboards()


