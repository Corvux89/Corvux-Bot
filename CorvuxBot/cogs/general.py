import logging

import discord.errors
import discord.utils
from os import listdir
from discord.commands import Option
from discord.ext import commands
from discord.ext.commands import Context
from CorvuxBot.bot import CorvuxBot
from CorvuxBot.helpers import *

log = logging.getLogger(__name__)


def setup(bot):
    bot.add_cog(General(bot))


class General(commands.Cog):
    bot: CorvuxBot

    def __init__(self, bot):
        self.bot = bot
        log.info(f'Cog \'general\' loaded')

    # Auditing Setup
    @staticmethod
    async def cog_before_invoke(ctx: Context):  # Log commands being run to better tie them to errors
        await cog_log(ctx, log)

    # Command: list
    @commands.slash_command(name="list",
                            description="Lists installed files for bot")
    @commands.check(is_admin)
    async def listCog(self, ctx):
        if not is_admin(ctx):
            await ctx.respond("Command for admin use only")
            log.warning('failure')
            return
        else:
            resp = []
            for file_name in listdir(COGS_DIR):
                if file_name.endswith('.py'):
                    resp.append(f'{COGS_PATH}.{file_name}')
            outputStr = "\n".join(resp)
            await ctx.respond(outputStr)

    # Command: load
    @commands.slash_command(name="load",
                            description="Cog loader")
    async def loadCog(self,
                      ctx: ApplicationContext,
                      ext: Option(str,
                                  "Cog to load",
                                  required=True,
                                  name="cog")):
        if not is_admin(ctx):
            await ctx.respond("Command for admin use only")
            return
        else:
            passfail, resp = load(self, ext)
            await ctx.respond(resp)

    # Command: unload
    @commands.slash_command(name="unload",
                            description="Cog remover")
    async def unloadCog(self,
                        ctx: ApplicationContext,
                        ext: Option(str,
                                    "Cog to unload",
                                    required=True,
                                    name="cog")):
        if not is_admin(ctx):
            await ctx.respond("Command for admin use only")
            return
        else:
            passfail, resp = unload(self, ext)
            await ctx.respond(resp)

    # Command: reload
    @commands.slash_command(name="reload",
                            description="Reload cogs")
    async def reloadCogs(self,
                         ctx: ApplicationContext,
                         ext: Option(str,
                                     "Cog to reload or 'ALL' to reload all",
                                     required=False,
                                     default="ALL",
                                     name="cog")):
        if not is_admin(ctx):
            await ctx.respond("Command for admin use only")
            return
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
    @commands.slash_command(name="break",
                            description="Inserts a break")
    async def lineBreak(self,
                        ctx: ApplicationContext):
        await ctx.delete()
        lBreak = discord.Embed()
        lBreak.add_field(name=discord.utils.escape_markdown('___________________________________________'),
                         value='\u200B',
                         inline=False)
        await ctx.respond(embed=lBreak)

