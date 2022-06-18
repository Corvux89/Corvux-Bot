import asyncio
import logging
from collections import defaultdict

import discord
from discord import InteractionMessage, SlashCommandGroup, ApplicationContext
from discord.ext import commands, tasks

from CorvuxBot.bot import CorvuxBot
from CorvuxBot.constants import *
from CorvuxBot.helpers import get_dashboard_by_channel_category_id, create_dashboard, get_excluded_channels, is_admin
from CorvuxBot.models.dashboard import Dashboard
from CorvuxBot.models.embeds import ErrorEmbed, dashboard_embed

log = logging.getLogger(__name__)


def setup(bot):
    bot.add_cog(Dashboard_Admin(bot))


# TODO: Refresh dashboard manually, add excluded channel, remove excluded channel
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
                                   checks=[is_admin])

    # Command: create_dashboard
    @dashboards.command(name="create_dashboard",
                        description="Creates a dashboard")
    async def create_dashboard(self,
                               ctx: ApplicationContext):
        if get_dashboard_by_channel_category_id(self.bot, ctx.channel.category_id) is not None:
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

        create_dashboard(self.bot, new_dashboard)
        await self.update_all_dashboards()

    @tasks.loop(hours=0.0, minutes=1.0, seconds=0.0)
    async def update_all_dashboards(self):
        log.info("Starting to update dashboards")
        valList = self.bot.sheet.dashboard_sheet.get_all_values()

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

    async def update_dashboard(self, dashboard: Dashboard):
        channels = dashboard.channels_to_check(self.bot)
        channels_dict = defaultdict(list)
        channels_dict.update({AVAILABLE: [], WAITING: [], BUSY: []})

        for channel in channels:
            status = ""
            last_message = channel.last_message
            if last_message is None:
                try:
                    lm_id = channel.last_message_id
                    last_message = await channel.fetch_message(lm_id) if lm_id is not None else None
                except discord.errors.HTTPException as e:
                    log.error(f'Skipping channel {channel.name}: [{e}]')

            if last_message is None or last_message.content == "```\n \n```":
                status = AVAILABLE
            elif any(item in last_message.raw_role_mentions for item in MAGEWRITE_ROLE):
                status = WAITING
            else:
                status = BUSY

            channels_dict[status].append(channel.mention)

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
