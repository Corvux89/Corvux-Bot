import logging
from collections import defaultdict
from itertools import zip_longest
from typing import Optional

import discord
from discord import CategoryChannel
from sqlalchemy.sql import FromClause

from CorvuxBot.constants import *

from CorvuxBot.models.dashboard import Dashboard
from CorvuxBot.models.embeds import dashboard_embed

log = logging.getLogger(__name__)


def get_dashboard_by_channel_category_id(self, category_channel_id: int) -> Optional[Dashboard]:
    if isinstance(category_channel_id, int):
        category_channel_id = str(category_channel_id)

    header_row = '1:1'
    target_cell = self.sheet.dashboard_sheet.find(category_channel_id, in_column=1)
    if not target_cell:
        return None

    dashboard_row = str(target_cell.row) + ":" + str(target_cell.row)
    data = self.sheet.dashboard_sheet.batch_get([header_row, dashboard_row])

    data_dict = dict(
        zip_longest(data[0][0], data[1][0]) if len(data[0][0]) > len(data[1][0]) else zip(data[0][0], data[1][0]))
    dashboard = Dashboard.from_dict(data_dict)
    return Dashboard.from_dict(data_dict)


async def create_dashboard(self, dashboard: Dashboard):
    dashboard_data = [
        str(dashboard.category_channel_id),
        str(dashboard.dashboard_post_channel_id),
        str(dashboard.dashboard_post_id),
        "|".join(filter(None, (str(c) for c in dashboard.excluded_channel_ids)))
    ]

    log.info(f'Appending new dashboard to sheet with data {dashboard_data}')
    self.sheet.dashboard_sheet.append_row(dashboard_data,
                                          value_input_option='USER_ENTERED',
                                          insert_data_option='INSERT_ROWS',
                                          table_range='A2')


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


def dashboard_category_filter2(self, category:CategoryChannel) -> FromClause:
    categories = c

def dashboard_category_filter(self, category: CategoryChannel) -> bool:
    categories = self.sheet.dashboard_sheet.col_values(1)
    del categories[0]

    return str(category.id) in categories
