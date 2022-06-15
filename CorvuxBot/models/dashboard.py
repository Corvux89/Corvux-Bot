from time import perf_counter
from typing import List, Dict, Any, Optional
from discord import CategoryChannel, Bot, Message, TextChannel
from CorvuxBot.sheets_client import GSheetsClient
from itertools import zip_longest
from CorvuxBot.contants import *

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
        dashboard = cls(category_channel_id=int(dashboard_dict["category_channel_id"]),
                        dashboard_post_channel_id=int(dashboard_dict["dashboard_post_channel_id"]),
                        dashboard_post_id=int(dashboard_dict["dashboard_post_id"]),
                        excluded_channel_ids=dashboard_dict["excluded_channel_ids"])
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
            return list(filter(lambda c: c.id not in self.excluded_channel_ids, category.text_channels))
        return []


class dashboards(GSheetsClient):
    sheets: GSheetsClient

    def __init__(self):
        super(dashboards, self).__init__()
        self.sheets = GSheetsClient

        start = perf_counter()
        self.dashboard_sheet = self.corvux_workbook.worksheet("Dashboard")
        end = perf_counter()
        print(f'Time to load dashboard sheet: {end - start}s')

    def get_dashboard_by_channel_category_id(self,category_channel_id: int) -> Optional[Dashboard]:
        if isinstance(category_channel_id, int):
            category_channel_id = str(category_channel_id)

        header_row = '1:1'
        target_cell = self.dashboard_sheet.find(category_channel_id, in_column=1)
        if not target_cell:
            return None

        dashboard_row = str(target_cell.row) + ":" + str(target_cell.row)
        data = self.dashboard_sheet.batch_get([header_row, dashboard_row])
        data_dict = {}

        data_dict = dict(zip_longest(data[0][0],data[1][0]) if len(data[0][0]) > len(data[1][0]) else zip(data[0][0], data[1][0]))


        return Dashboard.from_dict(data_dict)

    def create_dashboard(self, dashboard: Dashboard):
        dashboard_data = [
            str(dashboard.category_channel_id),
            str(dashboard.dashboard_post_channel_id),
            str(dashboard.dashboard_post_id),
            "|".join(str(c) for c in dashboard.excluded_channel_ids)
        ]

        print(f'Appending new dashboard to sheet with data {dashboard_data}')
        self.dashboard_sheet.append_row(dashboard_data,
                                        value_input_option='USER_ENTERED',
                                        insert_data_option='INSERT_ROWS',
                                        table_range='A2')