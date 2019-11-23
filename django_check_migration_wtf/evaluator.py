from typing import List

from django_check_migration_wtf.exceptions import SQLRuleError
from django_check_migration_wtf.rules import AbstractSQLRule


class SQLRuleEvaluator(object):
    def __init__(self):
        self.rules: List[AbstractSQLRule] = []

    def evaluate(self, sql_sentence: str):
        for rule in self.rules:
            if rule.is_match(sql_sentence):
                raise SQLRuleError(rule.error_info)
