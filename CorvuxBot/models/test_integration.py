import sqlalchemy as sa
from sqlalchemy import Column, Integer, TEXT
from sqlalchemy.orm import declarative_base

db = declarative_base()
metadata = sa.MetaData()

test_integration_table = sa.Table(
    "test_integration",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement='auto'),
    Column("name", TEXT, nullable=True)
)