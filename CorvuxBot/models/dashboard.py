import logging
from time import perf_counter
from typing import List, Dict, Any, Optional

import sqlalchemy as sa
from discord import CategoryChannel, Bot, Message, TextChannel
from sqlalchemy import BigInteger, Column, TEXT
from sqlalchemy.orm import declarative_base

from CorvuxBot.sheets_client import GSheetsClient
from itertools import zip_longest

log = logging.getLogger(__name__)


class Dashboard(object):
    category_channel_id: int
    dashboard_post_channel_id: int
    dashboard_post_id: int
    excluded_channel_ids: List[int]

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def from_dict(cls,
                  dashboard_dict: Dict[str, Any]):
        dashboard = cls(category_channel_id=int(dashboard_dict["Category Channel ID"]),
                        dashboard_post_channel_id=int(dashboard_dict["Dashboard Post Channel ID"]),
                        dashboard_post_id=int(dashboard_dict["Dashboard Post ID"]),
                        excluded_channel_ids=dashboard_dict["Excluded Channels"].split("|"))
        return dashboard

    def get_category_channel(self, bot: Bot) -> CategoryChannel | None:
        return bot.get_channel(self.category_channel_id)

    async def get_pinned_post(self, bot: Bot) -> Message | None:
        channel = bot.get_channel(self.dashboard_post_channel_id)
        if channel is not None:
            return await channel.fetch_message(self.dashboard_post_id)
        return None

    def channels_to_check(self, bot: Bot) -> List[TextChannel]:
        category: CategoryChannel = bot.get_channel(self.category_channel_id)
        if category is not None:
            return list(filter(lambda c: str(c.id) not in self.excluded_channel_ids, category.text_channels))
        return []


db = declarative_base()
metadata = sa.MetaData()


