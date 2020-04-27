from unittest import mock

import pytest

from django_check_migration_wtf.rules import AbstractSQLRule
from django_check_migration_wtf import psql


class TestAbstractSQLRule(object):
    @pytest.mark.parametrize('sql_sentence,expected',
                             [('test', True),
                              ('TEST', True),
                              ('bad', False)]
                             )
    @mock.patch.multiple('django_check_migration_wtf.rules.AbstractSQLRule', __abstractmethods__=set())
    @mock.patch('django_check_migration_wtf.rules.AbstractSQLRule.pattern',
                new_callable=mock.PropertyMock(return_value='test')
                )
    def test_is_match_true(self, _, sql_sentence, expected):
        rule = AbstractSQLRule()
        assert rule.is_match(sql_sentence) == expected


class TestRenameColumnSQLRule:
    def test_is_match(self):
        rule = psql.RenameColumnSQLRule()

        assert rule.is_match('ALTER TABLE test RENAME COLUMN column_a TO column_b;')


class TestRenameTableSQLRule:
    def test_is_match(self):
        rule = psql.RenameTableSQLRule()

        assert rule.is_match('ALTER TABLE test RENAME TO column_b;')


class TestAddColumnNotNullSQLRule:
    @pytest.mark.parametrize('sql_sentence', [
        'ALTER TABLE test ADD COLUMN column_test double precision DEFAULT 1.0 NOT NULL;',
        'ALTER TABLE test ADD COLUMN column_test double precision NOT NULL DEFAULT 1.0;',
        'ALTER TABLE test ADD COLUMN column_test integer NOT NULL;',
    ])
    def test_is_match(self, sql_sentence):
        rule = psql.AddColumnNotNullSQLRule()

        assert rule.is_match(sql_sentence)


class TestAddColumnDefaultSQLRule:
    @pytest.mark.parametrize('sql_sentence', [
        'ALTER TABLE test ADD COLUMN column_test double precision DEFAULT 1.0 NOT NULL;',
        'ALTER TABLE test ADD COLUMN column_test double precision NOT NULL DEFAULT 1.0;',
        'ALTER TABLE test ADD COLUMN column_test integer DEFAULT 1;',
    ])
    def test_is_match(self, sql_sentence):
        rule = psql.AddColumnDefaultSQLRule()

        assert rule.is_match(sql_sentence)


class TestAddColumnPrimaryKeySQLRule:
    @pytest.mark.parametrize('sql_sentence', [
        'ALTER TABLE test ADD COLUMN column_test integer DEFAULT 1 PRIMARY KEY NOT NULL;',
        'ALTER TABLE test ADD COLUMN column_test double precision NOT NULL PRIMARY KEY;',
        'ALTER TABLE test ADD COLUMN column_test double precision PRIMARY KEY;',
    ])
    def test_is_match(self, sql_sentence):
        rule = psql.AddColumnPrimaryKeySQLRule()

        assert rule.is_match(sql_sentence)


class TestAddColumnUniqueSQLRule:
    @pytest.mark.parametrize('sql_sentence', [
        'ALTER TABLE test ADD COLUMN column_test integer DEFAULT 1 UNIQUE NOT NULL;',
        'ALTER TABLE test ADD COLUMN column_test double precision NOT NULL UNIQUE;',
        'ALTER TABLE test ADD COLUMN column_test double precision UNIQUE;',
    ])
    def test_is_match(self, sql_sentence):
        rule = psql.AddColumnUniqueSQLRule()

        assert rule.is_match(sql_sentence)


class TestAlterColumnTypeSQLRule:
    @pytest.mark.parametrize('sql_sentence', [
        'ALTER TABLE test ALTER COLUMN column_test TYPE integer;',
        'ALTER TABLE test ALTER COLUMN column_test SET DATA TYPE integer;',
        'ALTER TABLE test ALTER COLUMN column_test TYPE varchar(11) USING a::varchar(11);',
        'ALTER TABLE test ALTER COLUMN column_test SET DATA TYPE varchar(11) USING a::varchar(11);',
        'ALTER TABLE test ALTER COLUMN column_test SET DATA TYPE varchar(11) USING a::varchar(11), ALTER COLUMN "column_test" DROP NOT NULL;',
    ])
    def test_is_match(self, sql_sentence):
        rule = psql.AlterColumnTypeSQLRule()

        assert rule.is_match(sql_sentence)


class TestAlterColumnAddConstraintSQLRule:
    @pytest.mark.parametrize('sql_sentence', [
        'ALTER TABLE test ADD CONSTRAINT constraint_test CHECK (char_length(column_test) = 5);',
        'ALTER TABLE test ADD CONSTRAINT constraint_test FOREIGN KEY (column_test) REFERENCES column_test (column_test) MATCH FULL;',
        'ALTER TABLE test ADD CONSTRAINT constraint_test UNIQUE (column_test_1, column_test_2);',
        'ALTER TABLE test ADD CONSTRAINT constraint_test PRIMARY KEY (column_test_1);',
        'ALTER TABLE test ADD CONSTRAINT "not valid constraint_test" PRIMARY KEY (column_test_1);',
        'ALTER TABLE test ADD CONSTRAINT "using index constraint_test" PRIMARY KEY (column_test_1);',
        'ALTER TABLE test ADD CONSTRAINT "ADD CONSTRAINT using index constraint_test" PRIMARY KEY (column_test_1);',
    ])
    def test_is_match(self, sql_sentence):
        rule = psql.AlterColumnAddConstraintSQLRule()

        assert rule.is_match(sql_sentence)

    @pytest.mark.parametrize('sql_sentence', [
        'ALTER TABLE test ADD CONSTRAINT constraint_test CHECK (char_length(column_test) = 5) NOT VALID;',
        'ALTER TABLE test ADD CONSTRAINT constraint_test CHECK (char_length(column_test) = 5) NOT VALID ;',
        'ALTER TABLE test ADD CONSTRAINT constraint_test FOREIGN KEY (column_test) REFERENCES column_test (column_test) MATCH FULL NOT VALID;',
        'ALTER TABLE test ADD CONSTRAINT constraint_test PRIMARY KEY USING INDEX index_test;',
        'ALTER TABLE test ADD CONSTRAINT constraint_test UNIQUE USING INDEX index_test ;',
    ])
    def test_not_match(self, sql_sentence):
        rule = psql.AlterColumnAddConstraintSQLRule()

        assert not rule.is_match(sql_sentence)


class TestAlterColumnAddPrimaryKeySQLRule:
    @pytest.mark.parametrize('sql_sentence', [
        'ALTER TABLE test ADD PRIMARY KEY (column_test);',
    ])
    def test_is_match(self, sql_sentence):
        rule = psql.AlterColumnAddPrimaryKeySQLRule()

        assert rule.is_match(sql_sentence)


class TestCreateIndexSQLRule:
    @pytest.mark.parametrize('sql_sentence', [
        'CREATE INDEX index_test on test (column_test);',
        'CREATE UNIQUE INDEX index_test on test (column_test);',
        'CREATE UNIQUE INDEX concurrently_test on test (column_test);',
        'CREATE UNIQUE INDEX "concurrently test" on test (column_test);',
    ])
    def test_is_match(self, sql_sentence):
        rule = psql.CreateIndexSQLRule()

        assert rule.is_match(sql_sentence)\


    @pytest.mark.parametrize('sql_sentence', [
        'CREATE INDEX CONCURRENTLY index_test on test (column_test);',
        'CREATE UNIQUE INDEX CONCURRENTLY index_test on test (column_test);',
    ])
    def test_is_not_match(self, sql_sentence):
        rule = psql.CreateIndexSQLRule()

        assert not rule.is_match(sql_sentence)