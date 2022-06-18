import logging
from itertools import zip_longest
from typing import Optional

from CorvuxBot.models.dashboard import Dashboard

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

    return Dashboard.from_dict(data_dict)


def create_dashboard(self, dashboard: Dashboard):
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
