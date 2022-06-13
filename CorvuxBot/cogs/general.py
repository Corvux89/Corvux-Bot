import datetime
import discord.errors
from os import listdir
from discord import ApplicationContext
from discord.ext import commands, tasks
from discord.ext.commands import Context
from CorvuxBot.bot import CorvuxBot, is_admin
from discord.commands import Option


def setup(bot):
    bot.add_cog(General(bot))


class General(commands.Cog):
    bot: CorvuxBot

    def __init__(self, bot):
        self.bot = bot
        print(f'Cog \'General\' loaded')

    @staticmethod
    async def cog_before_invoke(ctx: Context):  # Log commands being run to better tie them to errors
        print(f"{datetime.datetime.now}: Command [ /{ctx.command.qualified_name} ] initiated by member "
              f"[ {ctx.author.name}#{ctx.author.discriminator}, id: {ctx.author.id} ]")

    @commands.slash_command(name="list",
                            description="Lists installed files for bot")
    async def listCog(self, ctx):
        if not is_admin(ctx):
            await ctx.respond("Command for admin use only")
            return
        else:
            for file_name in listdir('./CorvuxBot/cogs'):
                if file_name.endswith('.py'):
                    await ctx.respond(f'CorvuxBot.cogs.{file_name}')

    @commands.slash_command(name="load",
                            description="Cog loader")
    async def loadCog(self,
                      ctx: ApplicationContext,
                      ext: Option(str,
                                  "Cog to load",
                                  required=True,
                                  name = "cog")):
        if not is_admin(ctx):
            await ctx.respond("Command for admin use only")
            return
        else:
            try:
                self.bot.load_extension(f'CorvuxBot.cogs.{ext}')
            except discord.errors.ExtensionAlreadyLoaded:
                await ctx.respond(f'{ext} already loaded.')
                return
            except discord.errors.ExtensionNotLoaded or discord.errors.ExtensionFailed:
                await ctx.respond(f'{ext} not loaded.')
                return
            except discord.errors.ExtensionNotFound:
                await ctx.respond(f'{ext} not found.')
                return
            await ctx.respond(f'{ext} loaded')

    @commands.slash_command(name="unload",
                            description="Cog remover")
    async def unloadCog(self,
                        ctx: ApplicationContext,
                        ext: Option(str,
                                    "Cog to unload",
                                    required=True,
                                    name="cog")):
        await ctx.send(ext)
        if not is_admin(ctx):
            await ctx.respond("Command for admin use only")
            return
        else:
            self.bot.unload_extension(f'CorvuxBot.cogs.{ext}')
            await ctx.respond("Cog Unloaded")
