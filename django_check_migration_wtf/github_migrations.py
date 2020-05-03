import re
from typing import List, Tuple, Optional

from django.conf import settings
from github import Github
from github.Comparison import Comparison
from github.File import File
from github.Repository import Repository


class GithubMigrations:
    FILE_STATUS_ADDED = 'added'
    FILE_STATUS_MODIFIED = 'modified'
    FILE_STATUS = (FILE_STATUS_ADDED, FILE_STATUS_MODIFIED,)

    def __init__(self, commit_hash: str, base_branch: str):
        self.g = Github(settings.CHECK_MIGRATION_WTF_GITHUB_TOKEN)
        self.repo: Repository = self.g.get_repo(settings.CHECK_MIGRATION_WTF_REPO_NAME)
        self.comp: Comparison = self.repo.compare(base_branch, commit_hash)
        self.migration_name_regex = re.compile(r'(?P<path>.*)/migrations/(?P<migration_name>.*).py\Z')

    @property
    def migrations(self) -> List[Tuple[str, str]]:
        migrations: List[Tuple[str, str]] = []
        file: File

        for file in self.comp.files:
            migration_name = self.get_migration_name(file.filename)
            if file.status not in self.FILE_STATUS or migration_name is None:
                continue

            migrations.append((file.filename, migration_name))

        return migrations

    def get_migration_name(self, filename: str) -> Optional[str]:
        m = self.migration_name_regex.match(filename)
        return m.group('migration_name') if m else None
