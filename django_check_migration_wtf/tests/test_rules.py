from unittest import mock

import pytest

from django_check_migration_wtf.rules import AbstractSQLRule


class TestAbstractSQLRule(object):
    @pytest.mark.parametrize('sql_sentence,expected',
                             [('test', True),
                              ('bad', False)]
                             )
    @mock.patch.multiple('django_check_migration_wtf.rules.AbstractSQLRule', __abstractmethods__=set())
    @mock.patch('django_check_migration_wtf.rules.AbstractSQLRule.pattern',
                new_callable=mock.PropertyMock(return_value='test')
                )
    def test_is_match_true(self, _, sql_sentence, expected):
        rule = AbstractSQLRule()
        assert rule.is_match(sql_sentence) == expected
