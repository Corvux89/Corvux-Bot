import logging
from time import perf_counter
import aiopg.sa
from aiopg.sa import create_engine
from discord.ext import commands
from CorvuxBot.constants import DATABASE_URL
from CorvuxBot.models.dashboard import dashboard_table
from CorvuxBot.sheets_client import GSheetsClient
from sqlalchemy.schema import CreateTable
from CorvuxBot.models.test_integration import test_integration_table

log = logging.getLogger(__name__)


async def create_table(conn: aiopg.sa.SAConnection):
    await conn.execute(CreateTable(test_integration_table, if_not_exists=True))
    await conn.execute(CreateTable(dashboard_table, if_not_exists=True))


class CorvuxBot(commands.Bot):
    sheets: GSheetsClient
    db: aiopg.sa.Engine

    def __init__(self, **options):
        super(CorvuxBot, self).__init__(**options)
        self.sheet = GSheetsClient()

    async def on_ready(self):
        start = perf_counter()
        self.db = await create_engine(DATABASE_URL)
        end = perf_counter()

        log.info(f'Time to create db engine: {end - start}s')

        async with self.db.acquire() as conn:
            await create_table(conn)

        log.info("logged in as")
        log.info(self.user.name)
        log.info(self.user.id)
        log.info("-----")
