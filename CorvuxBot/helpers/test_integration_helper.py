from CorvuxBot.models.test_integration import test_integration_table
from sqlalchemy.sql.selectable import FromClause, TableClause


def insert_new_test(name: str) -> TableClause:
    return test_integration_table.insert().values(
        name=name
    )
