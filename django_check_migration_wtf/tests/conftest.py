import pytest

from django_check_migration_wtf.rules import AbstractSQLRule


@pytest.fixture(scope="class")
def dummy_sql_rule():
    class DummySQLRule(AbstractSQLRule):

        @property
        def pattern(self) -> str:
            return 'dummy'

        @property
        def error_info(self) -> str:
            return 'Dummy match'

    return DummySQLRule()
