import logging

import discord.errors
import discord.utils
from os import listdir

from discord import ApplicationContext, BaseActivity
from discord.commands import Option, SlashCommandGroup
from discord.ext import commands
from CorvuxBot.bot import CorvuxBot
from CorvuxBot.helpers import load, unload, is_admin, insert_new_test
from CorvuxBot.constants import *

log = logging.getLogger(__name__)


def setup(bot):
    bot.add_cog(General(bot))


class General(commands.Cog):
    bot: CorvuxBot

    def __init__(self, bot):
        self.bot = bot
        log.info(f'Cog \'general\' loaded')

    admin = SlashCommandGroup(name="admin",
                              description="Bot administrative commands",
                              checks=[is_admin],
                              hidden=False)

    @admin.command(name="rubberduck")
    async def test_command(self,
                           ctx: ApplicationContext):
        await ctx.respond("Yup")

    # Command: list
    @admin.command(name="list",
                   description="Lists installed files for bot")
    async def listCog(self, ctx):
        resp = []
        for file_name in listdir(COGS_DIR):
            if file_name.endswith('.py'):
                resp.append(f'{COGS_PATH}.{file_name}')
        outputStr = "\n".join(resp)
        await ctx.respond(outputStr)

    # Command: load
    @admin.command(name="load",
                   description="Cog loader")
    async def loadCog(self,
                      ctx: ApplicationContext,
                      ext: Option(str,
                                  "Cog to load",
                                  required=True,
                                  name="cog")):
        passfail, resp = load(self, ext)
        await ctx.respond(resp)

    # Command: unload
    @admin.command(name="unload",
                   description="Cog remover")
    async def unloadCog(self,
                        ctx: ApplicationContext,
                        ext: Option(str,
                                    "Cog to unload",
                                    required=True,
                                    name="cog")):
        passfail, resp = unload(self, ext)
        await ctx.respond(resp)

    # Command: reload
    @admin.command(name="reload",
                   description="Reload cogs")
    async def reloadCogs(self,
                         ctx: ApplicationContext,
                         ext: Option(str,
                                     "Cog to reload or 'ALL' to reload all",
                                     required=False,
                                     default="ALL",
                                     name="cog")):
        if str(ext).upper() == 'ALL':
            responses = []
            for file_name in listdir(COGS_DIR):
                if file_name.endswith('.py'):
                    ext = file_name.replace('.py', '')
                    unloadPass, resp = unload(self, ext)
                    if not unloadPass:
                        responses.append(resp)
                        continue
                    loadPass, resp = load(self, ext)
                    responses.append(resp)

            outputStr = "\n".join(responses)
            await ctx.respond(f'```Reload Results: \n{outputStr}```')

    # Command: break
    @admin.command(name="insert",
                   description="Inserts a break")
    async def lineBreak(self,
                        ctx: ApplicationContext,
                        name: Option(str,
                                     description="Something",
                                     name="name",
                                     required=True)):
        await ctx.defer()
        async with self.bot.db.acquire() as conn:
            await conn.execute(insert_new_test(name))

        await ctx.respond("coool cool cool cool")

    # Command: chanSay
    @admin.command(name="chan_say",
                   description="Low-Level send message")
    async def chanSay(self,
                      ctx: ApplicationContext,
                      channel,
                      message: str):
        await self.bot.http.send_message(int(channel), message)
        await ctx.respond("Message sent")

    # Command: change_presence
    @admin.command(name="change_game_presence",
                   description="Change bot presence")
    async def change_game_presence(self,
                                   ctx: ApplicationContext,
                                   activity: Option(str,
                                                    "Activity",
                                                    default=None),
                                   status: Option(str,
                                                  "Status",
                                                  default="Online")):
        game = discord.Game(activity)
        await self.bot.change_presence(activity=game, status=status)
        await ctx.respond("Done", ephemeral=True)
