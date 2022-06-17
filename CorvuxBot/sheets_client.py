import logging
import json
import gspread
from time import perf_counter
from CorvuxBot.constants import *

log = logging.getLogger(__name__)


class GSheetsClient(object):
    def __init__(self):
        start = perf_counter()
        self.__auth = gspread.service_account_from_dict(json.loads(GOOGLE_SERVICE_ACCOUNT))
        end = perf_counter()
        log.info(f'Time to load auth: {end - start}s')

        # TODO: Do we really need to do this everytime we extend the client or can we just do it first time?

        # Open Workbook
        start = perf_counter()
        self.corvux_workbook = self.__auth.open_by_key(WORKBOOK_ID)
        end = perf_counter()
        log.info(f'Time to load workbook: {end - start}s')

    def reload(self):
        self.__init__()
