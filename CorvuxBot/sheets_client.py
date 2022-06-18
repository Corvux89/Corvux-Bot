import logging
import json
from typing import Optional

import gspread
from time import perf_counter
from CorvuxBot.constants import *
from CorvuxBot.models.characters import PlayerCharacter

log = logging.getLogger(__name__)


class GSheetsClient(object):
    def __init__(self):
        start = perf_counter()
        self.__auth = gspread.service_account_from_dict(json.loads(GOOGLE_SERVICE_ACCOUNT))
        end = perf_counter()
        log.info(f'Time to load auth: {end - start}s')

        # Open Workbook
        start = perf_counter()
        self.corvux_workbook = self.__auth.open_by_key(WORKBOOK_ID)
        end = perf_counter()
        log.info(f'Time to load workbook: {end - start}s')

        # Open sheets
        start = perf_counter()
        self.char_sheet = self.corvux_workbook.worksheet("Characters")
        self.dashboard_sheet = self.corvux_workbook.worksheet("Dashboard")
        self.reactions_sheet = self.corvux_workbook.worksheet("Reactions and Roles")
        end = perf_counter()
        log.info(f'Time to load worksheets: {end - start}s')

    def reload(self):
        self.__init__()
