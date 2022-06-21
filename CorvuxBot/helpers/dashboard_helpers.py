import logging
from collections import defaultdict
import discord
from sqlalchemy.sql import FromClause
from CorvuxBot.constants import *
from CorvuxBot.models.dashboard import Dashboard, dashboard_table, dashboard_schema
from CorvuxBot.models.embeds import dashboard_embed
import psycopg2

log = logging.getLogger(__name__)




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

async def get_dashboard_by_channel_category_id(self, category_channel_id: int) -> Dashboard:
    async with self.bot.db.acquire() as conn:
        data = await conn.execute(get_dashboard_by_channel_category_id_from(category_channel_id))
        row = await data.first()

    if row is None:
        return None

    dashboard: Dashboard = dashboard_schema().load(row)

    return dashboard





# Queries
def get_dashboard_by_channel_category_id_from(category_channel_id: int) -> FromClause:
    return dashboard_table.select().where(
        dashboard_table.c.category_channel_id == category_channel_id
    )


def insert_new_dashboard(dashboard: Dashboard):
    return dashboard_table.insert().values(
        category_channel_id=dashboard.category_channel_id,
        dashboard_post_channel_id=dashboard.dashboard_post_channel_id,
        dashboard_post_id=dashboard.dashboard_post_id,
        excluded_channel_ids=dashboard.excluded_channel_ids
    )


def get_all_dashboards() -> FromClause:
    return dashboard_table.select()


def update_excluded_channels(dashboard: Dashboard):
    return dashboard_table.update() \
        .where(dashboard_table.c.category_channel_id == dashboard.category_channel_id) \
        .values(excluded_channel_ids=dashboard.excluded_channel_ids)
