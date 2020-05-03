import pytest

from django_check_migration_wtf.evaluator import SQLRuleEvaluator
from django_check_migration_wtf.exceptions import SQLRuleError


class TestSQLRuleEvaluator(object):
    def test_evaluate_raise_sql_rule_error(self, dummy_sql_rule):
        evaluator = SQLRuleEvaluator()
        evaluator.rules.append(dummy_sql_rule)
        with pytest.raises(SQLRuleError, match=dummy_sql_rule.error_info):
            evaluator.evaluate('dummy')

    def test_evaluate_ok(self, dummy_sql_rule):
        evaluator = SQLRuleEvaluator()
        evaluator.rules.append(dummy_sql_rule)
        assert evaluator.evaluate('good') is None
