import faulthandler
import logging
import sys
import discord
from CorvuxBot.bot import CorvuxBot
from CorvuxBot.constants import *
from os import listdir
from discord.ext import commands

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


log_formatter = logging.Formatter("%(asctime)s %(name)s: %(message)s")
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(log_formatter)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
log = logging.getLogger("bot")

desc = "I have no idea what I'm doing"

bot = CorvuxBot(command_prefix=commands.when_mentioned_or(COMMAND_PREFIX),
                intents=intents,
                case_insensitive=True,
                help_command=None,
                description=desc,
                activity=discord.Game(name=GAME_NAME,
                                      type=GAME_TYPE),
                debug_guilds=DEBUG_GUILDS,
                allowed_mentions=discord.AllowedMentions.none())

for filename in listdir(COGS_DIR):
    if filename.endswith('.py'):
        bot.load_extension(f'{COGS_PATH}.{filename[:-3]}')


@bot.slash_command(name="ping",
                   description="Latency of the bot")
async def ping(ctx):
    await ctx.respond(f'Pong. Latency is {round(bot.latency)}ms.')

@bot.event
async def on_application_command(ctx):
    try:
        log.info(
            "cmd: chan {0.channel} ({0.channel.id}), serv: {0.guild} ({0.guild.id}),"
            "auth: {0.user} ({0.user.id}): {0.command}".format(ctx)
        )
    except AttributeError:
        log.info("Command in PM with {0.message.author} ({0.message.author.id}): {0.message.content}.".format(ctx))

@bot.event
async def on_ready():
    log.info("logged in as")
    log.info(bot.user.name)
    log.info(bot.user.id)
    log.info("-----")


@bot.event
async def on_resumed():
    log.info("resumed.")

@bot.event
async def on_command_error(error, *args, **kwargs):
    if isinstance(error, commands.CommandNotFound):
        return f'error'

@bot.event
async def on_application_command_error(ctx, error: Exception):
    if isinstance(error, commands.CommandNotFound):
        return f'error'

    elif isinstance(error, (commands.UserInputError, commands.NoPrivateMessage, ValueError)):
        return await ctx.respond(
            f"Error: {str(error)}\nUse `{ctx.prefix}help " + ctx.command.qualified_name + "` for help."
        )
    elif isinstance(error, commands.CheckFailure):
        msg = str(error) or "You are not allowed to run this command."
        return await ctx.respond(f"Error: {msg}")

    elif isinstance(error, commands.CommandOnCooldown):
        return await ctx.respond("This command is on cooldown for {:.1f} seconds.".format(error.retry_after))

    elif isinstance(error, commands.MaxConcurrencyReached):
        return await ctx.respond(str(error))

    elif isinstance(error.__cause__, AttributeError):
        return await ctx.respond(str(error))

    else:
        return await ctx.respond(str(error))

faulthandler.enable()
bot.state = "run"
bot.run(TOKEN)
