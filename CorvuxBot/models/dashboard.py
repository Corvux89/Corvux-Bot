import logging
from typing import List

import sqlalchemy as sa
from discord import CategoryChannel, Bot, Message, TextChannel
from sqlalchemy import BigInteger, Column, TEXT
from sqlalchemy.orm import declarative_base
from marshmallow import Schema, fields, post_load

log = logging.getLogger(__name__)


# Object
class Dashboard(object):
    category_channel_id: int
    dashboard_post_channel_id: int
    dashboard_post_id: int
    excluded_channel_ids: List[int]

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

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
            return list(filter(lambda c: c.id not in self.excluded_channel_ids, category.text_channels))
        return []


# Table
db = declarative_base()
metadata = sa.MetaData()

dashboard_table = sa.Table(
    "dashboards",
    metadata,
    Column("category_channel_id", BigInteger, primary_key=True, nullable=False),
    Column("dashboard_post_channel_id", BigInteger),
    Column("dashboard_post_id", BigInteger),
    Column("excluded_channel_ids", sa.ARRAY(TEXT))
)


# Schema
class dashboard_schema(Schema):
    category_channel_id = fields.Integer(data_key='category_channel_id', required=True)
    dashboard_post_channel_id = fields.Integer(data_key='dashboard_post_channel_id', required=True)
    dashboard_post_id = fields.Integer(data_key='dashboard_post_id', required=True)
    excluded_channel_ids = fields.List(fields.Integer, data_key='excluded_channel_ids', load_default=[])

    @post_load
    def make_dashboard(self, data, **kwargs):
        return Dashboard(**data)
