import datetime

import discord.errors
from discord.ext.commands import Context

from CorvuxBot.contants import *


def is_admin(ctx):
    return ctx.author.id in ADMIN_USERS


def unload(self, ext):
    try:
        self.bot.unload_extension(f'{COGS_PATH}.{ext}')
    except discord.errors.ExtensionError or discord.errors.ExtensionFailed:
        return False, f'{ext} error.'
    except discord.errors.ExtensionNotFound:
        return False, f'{ext} not found.'
    return True, f'{ext} unloaded.'


def load(self, ext):
    try:
        self.bot.load_extension(f'{COGS_PATH}.{ext}')
    except discord.errors.ExtensionAlreadyLoaded:
        return False, f'{ext} already loaded.'
    except discord.errors.ExtensionNotLoaded or discord.errors.ExtensionFailed or discord.errors.ExtensionError:
        return False, f'{ext} not loaded.'
    except discord.errors.ExtensionNotFound:
        return False, f'{ext} not found.'
    return True, f'{ext} loaded.'


async def cog_log(ctx: Context):  # Log commands being run to better tie them to errors
    print(f"{datetime.datetime.now()}: Command [ /{ctx.command.qualified_name} ] initiated by member "
          f"[ {ctx.author.name}#{ctx.author.discriminator}, id: {ctx.author.id} ]")
