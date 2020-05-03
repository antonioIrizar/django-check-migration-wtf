from unittest import mock

import pytest

from django_check_migration_wtf.rules import AbstractSQLRule
from django_check_migration_wtf.github_migrations import GithubMigrations


@pytest.fixture(scope='class')
def dummy_sql_rule():
    class DummySQLRule(AbstractSQLRule):

        @property
        def pattern(self) -> str:
            return 'dummy'

        @property
        def error_info(self) -> str:
            return 'Dummy match'

    return DummySQLRule()


@pytest.fixture(scope='function')
@mock.patch('django_check_migration_wtf.github_migrations.Github')
def github_migrations(_):
    return GithubMigrations('commit_hash', 'base_branch')
