import asyncio
import logging

import discord
from discord import ApplicationContext, InteractionMessage
from discord.ext import commands, tasks
from discord.ext.commands import Context

from CorvuxBot.bot import CorvuxBot
from CorvuxBot.constants import *
from CorvuxBot.helpers import cog_log, get_excluded_channels
from CorvuxBot.models.dashboard import Dashboard
from CorvuxBot.models.embeds import dashboard_embed, ErrorEmbed

log = logging.getLogger(__name__)


def setup(bot):
    bot.add_cog(Dashboard_Admin(bot))


# TODO: Refresh dashboard manually, add excluded channel, remove excluded channel
class Dashboard_Admin(commands.Cog):
    bot: CorvuxBot

    def __init__(self, bot):
        self.bot = bot
        log.info(f'Cog \'dashboard_admin\' loaded')

    # Auditing setup
    @staticmethod
    async def cog_before_invoke(ctx: Context):
        await cog_log(ctx, log)

    @commands.Cog.listener()
    async def on_ready(self):
        await asyncio.sleep(3.0)
        await self.update_all_dashboards.start()

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
                    log.error(f'Skipping channel {channel.name}: [{e}]')

            if last_message is None:
                status = GREY_QUESTION
            elif last_message.content == "```\n \n```":
                status = WHITE_CHECK
            elif any(item in last_message.raw_role_mentions for item in MAGEWRITE_ROLE):
                status = BOOKMARK
            else:
                status = RED_X

            channels_dict[channel.mention] = status
            try:
                original_msg = await dashboard.get_pinned_post(self.bot)
            except discord.errors.NotFound:
                log.warning(f'Message not found for msg id [{dashboard.dashboard_post_id}]')
                return

        if original_msg is not None:
            category = dashboard.get_category_channel(self.bot)
            await original_msg.edit(content='',
                                    embed=dashboard_embed(channels_dict, category.name))
        else:
            log.warning(f'Original message not found for msg id [{dashboard.dashboard_post_id}]')

    @tasks.loop(hours=0.0, minutes=1.0, seconds=0.0)
    async def update_all_dashboards(self):
        log.info("Starting to update dashboards")
        valList = self.bot.dashboards.dashboard_sheet.get_all_values()

        for r in valList[1:]:
            try:
                exc_c = [int(c) for c in list((r[3].split("|")))]
            except ValueError:
                exc_c = []
            try:
                dashboard = Dashboard(category_channel_id=int(r[0]),
                                      dashboard_post_channel_id=int(r[1]),
                                      dashboard_post_id=int(r[2]),
                                      excluded_channel_ids=exc_c)
            except discord.errors.NotFound or discord.errors:
                log.warning("Issue loading dashboard information")
            await self.update_dashboard(dashboard)
