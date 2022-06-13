import os
import discord
import discord.utils

from discord import Intents
from discord.ext import commands
from discord.commands import Option
from CorvuxBot.bot import CorvuxBot
from CorvuxBot.helpers import is_admin
from os import listdir
from discord.commands.context import ApplicationContext

intents = Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True

bot = CorvuxBot(command_prefix=os.environ['COMMAND_PREFIX'],
                intents=intents,
                case_insensitive=True,
                help_command=None,
                debug_guilds=[os.environ.get("GUILD", [])])

for filename in listdir('CorvuxBot/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'CorvuxBot.cogs.{filename[:-3]}')

@bot.slash_command(name="ping",
                   description="Latency of the bot")
async def ping(ctx):
    await ctx.respond(f'Pong. Latency is {round(bot.latency)}ms.')

bot.run(os.environ['BOT_TOKEN'])
