from unittest import mock

import pytest

from django_check_migration_wtf.github_migrations import GithubMigrations


class TestGithubMigrations:
    @pytest.mark.parametrize('filename',
                             ['/test/migrations/0001_32524.py',
                              'test/migrations/0001_32524.py',
                              'test2/test3/test/migrations/0001_32524.py', ]
                             )
    def test_get_migration_name(self, filename, github_migrations):
        assert github_migrations.get_migration_name(filename) == '0001_32524'

    @pytest.mark.parametrize('filename',
                             ['test/bad_migrations/0001_32524.py',
                              'test/migrations/0001_32524.py.back',
                              'test/migrations/0001_32524', ]
                             )
    def test_get_migration_name_return_none(self, filename, github_migrations):
        assert github_migrations.get_migration_name(filename) is None

    @pytest.mark.parametrize(
        'status, filename, expected',
        [
            ('bad', '/test/migrations/0001_32524.py', [],),
            (GithubMigrations.FILE_STATUS_ADDED, '/test/migrations/bad', []),
            (GithubMigrations.FILE_STATUS_ADDED, '/test/migrations/0001_32524.py', [('/test/migrations/0001_32524.py', '0001_32524')]),
            (GithubMigrations.FILE_STATUS_MODIFIED, '/test/migrations/0001_32524.py', [('/test/migrations/0001_32524.py', '0001_32524')]),
        ]
    )
    def test_migration(self, status, filename, expected, github_migrations):
        github_migrations.comp = mock.PropertyMock(files=[
            mock.MagicMock(
                status=status,
                filename=filename,
            )
        ])

        assert github_migrations.migrations == expected
