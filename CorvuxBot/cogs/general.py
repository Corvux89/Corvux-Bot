import discord.utils
import discord.errors
from os import listdir
from discord import ApplicationContext, Embed, TextChannel, InteractionMessage, Member
from discord.ext import commands, tasks
from CorvuxBot.bot import CorvuxBot
from CorvuxBot.models.dashboard import Dashboard
from CorvuxBot.models.embeds import ErrorEmbed, dashboard_embed
from CorvuxBot.helpers import *
from discord.commands import Option
from discord.ext.commands import Context
from CorvuxBot.contants import *

import json


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
                    if unloadPass == False:
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

    # Command: create_dashboard
    @commands.slash_command(name="create_dashboard",
                            description="Creates a dashboard")
    async def create_dashboard(self,
                               ctx: ApplicationContext):

        if self.bot.dashboards.get_dashboard_by_channel_category_id(ctx.channel.category_id) is not None:
            await ctx.respond(embed=ErrorEmbed(description="There is already a dashboard for this category. "
                                                           "Delete that before creating another."))
            return

        excluded_channels = get_excluded_channels(ctx, self.bot)

        interaction = await ctx.respond("Fetching dashboard data....")
        msg: InteractionMessage = await interaction.original_message()
        await msg.pin(reason=f"Dashboard for {ctx.channel.category.name} created by {ctx.author.name}")

        new_dashboard = Dashboard(category_channel_id=ctx.channel.category.id,
                                  dashboard_post_channel_id=ctx.channel.id,
                                  dashboard_post_id=msg.id,
                                  excluded_channel_ids=excluded_channels)

        self.bot.dashboards.create_dashboard(new_dashboard)
        print("Dashboard created")
        await self.update_all_dashboards()

    async def update_dashboard(self, dashboard: Dashboard):
        channels = dashboard.channels_to_check(self.bot)
        channels_dict = {}

        for channel in channels:
            last_message = channel.last_message
            if last_message is None:
                try:
                    lm_id = channel.last_message_id
                    last_message = await channel.fetch_message(lm_id) if lm_id is not None else None
                except discord.errors.HTTPException as e:
                    print(f'Skipping channel {channel.name}: [ {e} ]')

            if last_message is None:
                status = "<:grey_question:983576825294884924>"
            elif last_message.content == "```\n \n```":
                status = "<:white_check_mark:983576747381518396>"
            elif any(item in last_message.raw_role_mentions for item in MAGEWRITE_ROLE):
                status = "<:bookmark:986735232604598302>"
            else:
                status = "<:x:983576786447245312>"

            channels_dict[channel.mention] = status

            original_msg = await dashboard.get_pinned_post(self.bot)
            if original_msg is not None:
                category = dashboard.get_category_channel(self.bot)
                await original_msg.edit(content='',
                                        embed=dashboard_embed(channels_dict, category.name))
            else:
                print(f'Original message not found for msg id [ {dashboard.dashboard_post_id} ]')

    #TODO: Test task loop
    @tasks.loop(minutes=30.0)
    async def update_all_dashboards(self):
        print("Starting to update dashboards")
        valList = self.bot.dashboards.dashboard_sheet.get_all_values()

        for r in valList[1:]:
            dashboard = Dashboard(category_channel_id=int(r[0]),
                                  dashboard_post_channel_id=int(r[1]),
                                  dashboard_post_id=int(r[2]),
                                  excluded_channel_ids=[int(c) for c in list((r[3].split("|")))])
            await self.update_dashboard(dashboard)
