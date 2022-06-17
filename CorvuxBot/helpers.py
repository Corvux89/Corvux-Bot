from typing import List
import discord.errors
from discord import TextChannel, Bot, CategoryChannel, ApplicationContext
from CorvuxBot.constants import *


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


# TODO: Part of logging...but do better
async def cog_log(ctx: ApplicationContext, log):  # Log commands being run to better tie them to errors
    try:
        log.info(
            "cmd: chan {0.channel} ({0.channel.id}), serv: {0.guild} ({0.guild.id}),"
            "auth: {0.user} ({0.user.id}): {0.command}".format(ctx)
        )
    except AttributeError:
        log.info("Command in PM with {0.message.author} ({0.message.author.id}): {0.message.content}.".format(ctx))

