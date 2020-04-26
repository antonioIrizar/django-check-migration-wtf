from typing import List

from django.conf import settings

from django_check_migration_wtf.exceptions import SQLRuleError
from django_check_migration_wtf.rules import AbstractSQLRule
from . import psql


class SQLRuleEvaluator(object):
    def __init__(self):
        self.rules: List[AbstractSQLRule] = []

    def load_psql_rules(self):
        self.rules = [
            psql.RenameTableSQLRule(),
            psql.RenameColumnSQLRule(),
            psql.AddColumnNotNullSQLRule(),
            psql.AddColumnPrimaryKeySQLRule(),
            psql.AddColumnUniqueSQLRule(),
            psql.AlterColumnTypeSQLRule(),
            psql.AlterColumnAddPrimaryKeySQLRule(),
            psql.AlterColumnAddConstraintSQLRule(),
            psql.CreateIndexSQLRule(),
        ]

        psql_version = getattr(settings, 'CHECK_MIGRATION_WTF_PSQL_VERSION', 9)
        if psql_version < 11:
            self.rules.append(psql.AddColumnDefaultSQLRule())

    def evaluate(self, sql_sentence: str):
        for rule in self.rules:
            if rule.is_match(sql_sentence):
                raise SQLRuleError(rule.error_info)
