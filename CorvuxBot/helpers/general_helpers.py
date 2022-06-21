import logging
from typing import List
import discord.errors
from discord import TextChannel, Bot, CategoryChannel
from CorvuxBot.constants import *


log = logging.getLogger(__name__)


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
