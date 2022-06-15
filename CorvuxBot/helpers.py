import datetime
from itertools import islice
from typing import List

import discord.errors
from discord import TextChannel, Bot, CategoryChannel, ApplicationContext
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


def get_excluded_channels(self, bot: Bot) -> List[TextChannel]:
    category: CategoryChannel = bot.get_channel(self.channel.category_id)
    if category is not None:
        return EXCLUDED_CHANNElS.get(category.id)
    return []


async def cog_log(ctx: Context):  # Log commands being run to better tie them to errors
    print(f"{datetime.datetime.now()}: Command [ /{ctx.command.qualified_name} ] initiated by member "
          f"[ {ctx.author.name}#{ctx.author.discriminator}, id: {ctx.author.id} ]")


def split_dict(data, SIZE=10000):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield {k:data[k] for k in islice(it, SIZE)}
