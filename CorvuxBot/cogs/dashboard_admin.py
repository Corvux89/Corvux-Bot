import asyncio
import logging
import psycopg2
from discord import InteractionMessage, SlashCommandGroup, ApplicationContext, Option, CategoryChannel, TextChannel
from discord.ext import commands, tasks
from CorvuxBot.bot import CorvuxBot
from CorvuxBot.helpers import get_dashboard_by_channel_category_id, is_admin, update_dashboard, \
    insert_new_dashboard, get_all_dashboards, update_excluded_channels
from CorvuxBot.models.dashboard import Dashboard, dashboard_schema
from CorvuxBot.models.embeds import ErrorEmbed

log = logging.getLogger(__name__)


def setup(bot):
    bot.add_cog(Dashboard_Admin(bot))


# TODO: Completely compartmentalize API calls
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
                               ctx: ApplicationContext,
                               exclusion1: Option(TextChannel,
                                                  "First channel to exclude",
                                                  required=False,
                                                  default=None),
                               exclusion2: Option(TextChannel,
                                                  "Second channel to exclude",
                                                  required=False,
                                                  default=None),
                               exclusion3: Option(TextChannel,
                                                  "Third channel to exclude",
                                                  required=False,
                                                  default=None),
                               exclusion4: Option(TextChannel,
                                                  "Fourth channel to exclude",
                                                  required=False,
                                                  default=None),
                               exclusion5: Option(TextChannel,
                                                  "Fifth channel to exclude",
                                                  required=False,
                                                  default=None)
                               ):
        dashboard = await get_dashboard_by_channel_category_id(self, ctx.channel.category_id)
        if dashboard is not None:
            await ctx.respond(embed=ErrorEmbed(description="There is already a dashboard for this category. "
                                                           "Delete that before creating another."))
            return

        excluded_channels = list(set(filter(lambda c: c is not None,
                                            [exclusion1, exclusion2, exclusion3, exclusion4, exclusion5])))

        interaction = await ctx.respond("Fetching dashboard data....")
        msg: InteractionMessage = await interaction.original_message()
        await msg.pin(reason=f"Dashboard for {ctx.channel.category.name} created by {ctx.author.name}")

        new_dashboard = Dashboard(category_channel_id=ctx.channel.category.id,
                                  dashboard_post_channel_id=ctx.channel.id,
                                  dashboard_post_id=msg.id,
                                  excluded_channel_ids=[c.id for c in excluded_channels])
        try:
            async with self.bot.db.acquire() as conn:
                await conn.execute(insert_new_dashboard(new_dashboard))
        except psycopg2.Error:
            await msg.delete()
            await ctx.respond(ErrorEmbed(description="A database error was encountered. Aborting."))
            log.error(f"Issue creating dashboard for {ctx.channel.category} ({ctx.channel.category_id})")
            return
        else:
            log.error(f"Creating dashboard for {ctx.channel.category} ({ctx.channel.category_id})")
            await update_dashboard(self, new_dashboard)

    # Command: update_dashboard
    @dashboards.command(name="update_dashboard",
                        description="Updates a dashboard for a given CategoryChannel")
    async def update_dashboard(self,
                               ctx: ApplicationContext,
                               category: Option(CategoryChannel,
                                                description="Category channel to update",
                                                required=True)):
        dashboard = await get_dashboard_by_channel_category_id(self, category.id)
        if dashboard is None:
            await ctx.respond(embed=ErrorEmbed(description="This category currently doesn't have a dashboard. "
                                                           "Please pick another category or create one first."))
        await update_dashboard(self, dashboard)
        await ctx.respond("Complete", ephemeral=True)

    # Command: add_excluded_channel
    @dashboards.command(name="add_excluded_channel",
                        description="Add a channel to dashboard exclusions")
    async def add_excluded_channel(self,
                                   ctx: ApplicationContext,
                                   channel: Option(TextChannel,
                                                   "Channel to exclude",
                                                   required=True)):
        category_channel_id = channel.category.id

        dashboard = await get_dashboard_by_channel_category_id(self, category_channel_id)
        if dashboard is None:
            await ctx.respond(
                embed=ErrorEmbed(description="This channel's category currently doesn't have a dashboard."))
            return

        if channel.id in dashboard.excluded_channel_ids:
            await ctx.respond(embed=ErrorEmbed(description="Channel already excluded"))
            return
        await ctx.response.defer(ephemeral=True)
        dashboard.excluded_channel_ids.append(channel.id)

        async with self.bot.db.acquire() as conn:
            await conn.execute(update_excluded_channels(dashboard))

        await update_dashboard(self, dashboard)
        await ctx.respond("Complete", ephemeral=True)

    # Command: remove_excluded_channel
    @dashboards.command(name="remove_excluded_channel",
                        description="Remove an excluded channel")
    async def remove_excluded_channel(self,
                                      ctx: ApplicationContext,
                                      channel: Option(TextChannel,
                                                      "Channel to exclude",
                                                      required=True)):
        category_channel_id = channel.category.id

        dashboard = await get_dashboard_by_channel_category_id(self, category_channel_id)

        if dashboard is None:
            await ctx.respond(
                embed=ErrorEmbed(description="This channel's category currently doesn't have a dashboard."))
            return

        if channel.id not in dashboard.excluded_channel_ids:
            await ctx.respond(embed=ErrorEmbed(description="Channel not excluded"))
            return
        dashboard.excluded_channel_ids.remove(channel.id)

        async with self.bot.db.acquire() as conn:
            await conn.execute(update_excluded_channels(dashboard))

        await update_dashboard(self, dashboard)
        await ctx.respond("Complete", ephemeral=True)

    # Task Loop
    @tasks.loop(hours=0.0, minutes=30.0, seconds=0.0)
    async def update_all_dashboards(self):
        log.info("Starting to update dashboards")
        async with self.bot.db.acquire() as conn:
            async for row in conn.execute(get_all_dashboards()):
                dashboard: Dashboard = dashboard_schema().load(row)
                await update_dashboard(self, dashboard)
