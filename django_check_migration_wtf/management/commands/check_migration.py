from django.core.management.base import BaseCommand, CommandError
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor

from ...evaluator import SQLStatementsEvaluator
from ...github_migrations import GithubMigrations


class Command(BaseCommand):
    help = "Checks migrations without apply to know if they are secure to do without downtime"
    output_transaction = True

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)

        self.connection = connections[DEFAULT_DB_ALIAS]
        self.executor = MigrationExecutor(self.connection)
        self.loader = self.executor.loader
        self.error = False

    def add_arguments(self, parser):
        parser.add_argument(
            'app_label', nargs='*',
            help='App labels of applications to limit the check.',
        )

        parser.add_argument(
            '--github', nargs=2, type=str,
            help='Check migrations comparing hash of commit with name of base branch',
        )

    def handle(self, *args, **options):
        if options.get('github'):
            github_migrations = GithubMigrations(options['github'][0], options['github'][1])
            migrations = github_migrations.migrations
            for filename, migration_name in migrations:
                app_name = self.get_app_name(filename)
                self.evaluate_migration(app_name, migration_name)

        else:
            # Work out which apps have migrations and which do not
            graph = self.executor.loader.graph
            for app_name in self.loader.migrated_apps:
                for node in graph.leaf_nodes(app_name):
                    for plan_node in graph.forwards_plan(node):
                        # Mark it as applied/unapplied
                        if plan_node not in self.loader.applied_migrations:
                            self.evaluate_migration(plan_node[0], plan_node[1])

        if self.error:
            raise CommandError('WTF!!!!!!!!!!! Migrations are not secure.')

        self.stdout.write(self.style.SUCCESS('Migrations are secure.'))

    def evaluate_migration(self, app_label, migration_name):
        migration = self.loader.get_migration_by_prefix(app_label, migration_name)
        self.output_transaction = migration.atomic and self.connection.features.can_rollback_ddl

        plan = self.loader.graph.nodes[app_label, migration_name]
        sql_statements = self.executor.collect_sql([(plan, False)])

        self.stdout.write(self.style.MIGRATE_HEADING(f'App name: {app_label} - Migration: {migration_name}'))
        evaluator = SQLStatementsEvaluator(sql_statements)
        errors = evaluator.evaluate()

        for sql, error_info in errors:
            self.error = True
            self.stderr.write('    SQL is not secure to do without downtime.')
            self.stderr.write(f'    SQL sentence: {sql}', style_func=self.style.SQL_KEYWORD)
            self.stderr.write(f'    {error_info}', style_func=self.style.NOTICE)

        if not errors:
            self.stdout.write(self.style.SUCCESS('    Migration is secure.'))

    def get_app_name(self, filename) -> str:
        for app_name in self.loader.migrated_apps:
            path, _ = self.loader.migrations_module(app_name)
            path = path.replace('.', '/') + '/'
            if path in filename:
                return app_name

        raise ValueError('Cannot find the app name')
