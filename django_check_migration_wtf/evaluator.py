import re
from typing import List, Tuple, Optional

from django.conf import settings

from .exceptions import SQLRuleError
from .rules import AbstractSQLRule
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


class SQLStatementsEvaluator:
    SQL_COMMENT = '--'
    SQL_CREATE_TABLE = 'create table '

    def __init__(self, sql_statements):
        self.sql_statements = sql_statements
        self.name_create_tables = []
        self.sql_rule_evaluator = SQLRuleEvaluator()
        self.sql_rule_evaluator.load_psql_rules()
        self.create_rex = re.compile(r'^create .*table (if not exists )?(?P<name>(".*"|.*[^\s]*)) \(.*')

    def evaluate(self) -> List[Optional[Tuple[str, SQLRuleError]]]:
        errors = []
        sql_line: str
        for sql_line in self.sql_statements:
            sql_line = sql_line.lower()
            if self.is_comment(sql_line):
                continue
            if self.is_create_table(sql_line):
                self.name_create_tables.append(self.get_name_create_table(sql_line))
            if self.should_skip(sql_line):
                continue
            try:
                self.sql_rule_evaluator.evaluate(sql_line)
            except SQLRuleError as e:
                errors.append((sql_line, e))

        return errors

    def is_comment(self, sql_line: str) -> bool:
        return sql_line.startswith(self.SQL_COMMENT)

    def is_create_table(self, sql_line: str) -> bool:
        return sql_line.startswith(self.SQL_CREATE_TABLE)

    def should_skip(self, sql_line: str) -> bool:
        for name in self.name_create_tables:
            if name in sql_line:
                return True
        return False

    def get_name_create_table(self, sql_line: str) -> str:
        m = self.create_rex.match(sql_line)
        return m.group('name')
