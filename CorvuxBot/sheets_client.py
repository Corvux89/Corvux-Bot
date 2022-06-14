import os
import json
import gspread
from time import perf_counter

class GSheetsClient(object):
    def __init__(self):
        start = perf_counter()
        self.__auth = gspread.service_account_from_dict(json.loads(os.environ['GOOGLE_KEY_JSON']))
        end = perf_counter()
        print(f'Time to load auth: {end - start}s')

        #Open Workbook
        start = perf_counter()
        self.corvux_workbook = self.__auth.open_by_key((os.environ['SHEET_ID']))
        end = perf_counter()
        print(f'Time to load workbook: {end - start}s')

        def reload(self):
            self.__init__()
