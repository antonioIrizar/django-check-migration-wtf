from io import StringIO

import pytest
from django.core.management import call_command


@pytest.mark.django_db
class TestCommand(object):
    def test_command_output(self, capsys):

        out = StringIO()
        with capsys.disabled():
            call_command('migrate', 'test_app', '0001')
        call_command('check_migration', stdout=out)
        captured = capsys.readouterr()
        assert 'SQL is not secure to do without downtime' in captured.out

    def test_command_output_not_sql_insecure(self, capsys):

        out = StringIO()
        with capsys.disabled():
            call_command('migrate', 'test_app', '0002')
        call_command('check_migration', stdout=out)
        captured = capsys.readouterr()

        assert 'SQL is not secure to do without downtime' not in captured.out

    def test_command_github(self, capsys):
        out = StringIO()
        with capsys.disabled():
            call_command('migrate', 'test_app_github', '0001')
        call_command('check_migration', '--github', 'f6d560cb06b54d7f6f8ec94cf9a510632aed25fc', 'test-github-integration-without-migration-not-delete', stdout=out)
        captured = capsys.readouterr()

        assert 'SQL is not secure to do without downtime' in captured.out
