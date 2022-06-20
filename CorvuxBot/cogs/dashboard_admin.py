import asyncio
import logging

import discord
from discord import InteractionMessage, SlashCommandGroup, ApplicationContext, Option, CategoryChannel
from discord.ext import commands, tasks
from CorvuxBot.bot import CorvuxBot
from CorvuxBot.helpers import get_dashboard_by_channel_category_id, create_dashboard, get_excluded_channels, is_admin, \
    update_dashboard, dashboard_category_filter
from CorvuxBot.models.dashboard import Dashboard
from CorvuxBot.models.embeds import ErrorEmbed

log = logging.getLogger(__name__)


def setup(bot):
    bot.add_cog(Dashboard_Admin(bot))


# TODO: add excluded channel, remove excluded channel
class Dashboard_Admin(commands.Cog):
    bot: CorvuxBot

    def __init__(self, bot):
        self.bot = bot
        log.info(f'Cog \'dashboard_admin\' loaded')

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(3.0)
        await self.update_all_dashboards.start()

    dashboards = SlashCommandGroup(name="dashboards",
                                   description="Dashboard commands",
                                   checks=[is_admin],
                                   hidden=True)

    # Command: create_dashboard
    @dashboards.command(name="create_dashboard",
                        description="Creates a dashboard")
    async def create_dashboard(self,
                               ctx: ApplicationContext):
        if get_dashboard_by_channel_category_id(self.bot, ctx.channel.category_id) is not None:
            await ctx.respond(embed=ErrorEmbed(description="There is already a dashboard for this category. "
                                                           "Delete that before creating another."))
            return

        excluded_channels = get_excluded_channels(self)

        interaction = await ctx.respond("Fetching dashboard data....")
        msg: InteractionMessage = await interaction.original_message()
        await msg.pin(reason=f"Dashboard for {ctx.channel.category.name} created by {ctx.author.name}")

        new_dashboard = Dashboard(category_channel_id=ctx.channel.category.id,
                                  dashboard_post_channel_id=ctx.channel.id,
                                  dashboard_post_id=msg.id,
                                  excluded_channel_ids=excluded_channels)

        create_dashboard(self.bot, new_dashboard)
        await self.update_all_dashboards()

    # Command: update_dashboard
    @dashboards.command(name="update_dashboard",
                        description="Updates a dashboard for a given CategoryChannel")
    async def update_dashboard(self,
                               ctx: ApplicationContext,
                               category: Option(CategoryChannel,
                                                description="Category channel to update",
                                                required=True)):
        dashboard = Dashboard
        dashboard = get_dashboard_by_channel_category_id(self.bot, int(category.id)) # TODO: This keeps erroring
        if dashboard is None:
            await ctx.respond(embed=ErrorEmbed(description="This category currently doesn't have a dashboard. "
                                                           "Please pick another category or create one first."))
        await ctx.response.defer(ephemeral=True)
        await update_dashboard(self, dashboard)
        await ctx.respond("Dashboard update go BRRRRRR")


    @tasks.loop(hours=0.0, minutes=1.0, seconds=0.0)
    async def update_all_dashboards(self):
        log.info("Starting to update dashboards")
        valList = self.bot.sheet.dashboard_sheet.get_all_values()

        for r in valList[1:]:
            try:
                dashboard = Dashboard(category_channel_id=int(r[0]),
                                      dashboard_post_channel_id=int(r[1]),
                                      dashboard_post_id=int(r[2]),
                                      excluded_channel_ids=r[3])
            except discord.errors.NotFound or discord.errors:
                log.warning("Issue loading dashboard information")
            await update_dashboard(self, dashboard)
