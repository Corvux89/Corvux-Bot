from os import listdir
from discord import ApplicationContext, Embed
from discord.ext import commands
from CorvuxBot.bot import CorvuxBot
from CorvuxBot.helpers import *
from discord.commands import Option
from CorvuxBot.models.embeds import linebreak


def setup(bot):
    bot.add_cog(General(bot))


class General(commands.Cog):
    bot: CorvuxBot

    def __init__(self, bot):
        self.bot = bot
        print(f'Cog \'general\' loaded')

    # Auditing Setup
    @staticmethod
    async def cog_before_invoke(ctx: Context):  # Log commands being run to better tie them to errors
        await cog_log(ctx)

    # Command: list
    @commands.slash_command(name="list",
                            description="Lists installed files for bot")
    async def listCog(self, ctx):
        if not is_admin(ctx):
            await ctx.respond("Command for admin use only")
            return
        else:
            for file_name in listdir(COGS_DIR):
                if file_name.endswith('.py'):
                    await ctx.respond(f'{COGS_PATH}.{file_name}')

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
            passfail, resp = unload(self,ext)
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
                    unloadPass, resp = unload(self,ext)
                    if unloadPass == False:
                        responses.append(resp)
                        continue
                    loadPass, resp = load(self, ext)
                    responses.append(resp)

            outputStr = "\n".join(responses)
            await ctx.respond(f'```Reload Results: \n{outputStr}```')

    @commands.slash_command(name="break",
                            description="Inserts a break")
    async def lineBreak(self,
                    ctx: ApplicationContext):
        await ctx.delete()
        embed = discord.Embed.from_dict(linebreak())
        await ctx.send("No Clue")