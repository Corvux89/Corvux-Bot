import faulthandler
import logging
import sys

import discord
from discord import Intents, ApplicationContext, Reaction
from discord.ext.commands import CommandInvokeError

from CorvuxBot.bot import CorvuxBot
from CorvuxBot.constants import *
from os import listdir
from discord.ext import commands

# TODO: Better command logging and command error handling.

intents = discord.Intents(
    guilds=True,
    members=True,
    messages=True,
    reactions=True,
    bans=False,
    emojis=False,
    integrations=False,
    webhooks=False,
    invites=False,
    voice_states=False,
    presences=False,
    typing=False
)

desc = "I have no idea what I'm doing"

bot = CorvuxBot(command_prefix=COMMAND_PREFIX,
                intents=intents,
                case_insensitive=True,
                help_command=None,
                description=desc,
                activity=discord.Game(name=GAME_NAME,
                                      type=GAME_TYPE),
                debug_guilds=DEBUG_GUILDS)

for filename in listdir(COGS_DIR):
    if filename.endswith('.py'):
        bot.load_extension(f'{COGS_PATH}.{filename[:-3]}')


@bot.slash_command(name="ping",
                   description="Latency of the bot")
async def ping(ctx):
    await ctx.respond(f'Pong. Latency is {round(bot.latency)}ms.')


log_formatter = logging.Formatter("%(asctime)s %(name)s: %(message)s")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(log_formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
log = logging.getLogger("bot")


@bot.event
async def on_command(ctx: ApplicationContext):
    print(f'here')

@bot.event
async def on_application_command_error(error,ctx):
    print(f'here')

@bot.event
async def on_application_command(ctx):
    print(f'COMMANDY COMMAN')


@bot.event
async def on_ready():
    log.info("logged in as")
    log.info(bot.user.name)
    log.info(bot.user.id)
    log.info("-----")


@bot.event
async def on_resumed():
    log.info("resumed.")


faulthandler.enable()
bot.state = "run"
bot.run(TOKEN)
