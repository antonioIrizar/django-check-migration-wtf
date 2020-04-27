from typing import List

from django.core.management.base import (
    BaseCommand, )
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor

from ...evaluator import SQLRuleEvaluator, SQLStatementsEvaluator
from ...exceptions import SQLRuleError


class Command(BaseCommand):
    help = "Checks migrations without apply to know if they are secure to do without downtime"
    output_transaction = True

    def add_arguments(self, parser):
        parser.add_argument(
            'app_label', nargs='*',
            help='App labels of applications to limit the check.',
        )

    def handle(self, *args, **options):
        # Get the database we're operating from
        connection = connections[DEFAULT_DB_ALIAS]

        # Work out which apps have migrations and which do not
        executor = MigrationExecutor(connection)
        loader = executor.loader
        graph = executor.loader.graph
        for app_name in loader.migrated_apps:
            for node in graph.leaf_nodes(app_name):
                for plan_node in graph.forwards_plan(node):

                    migration = loader.get_migration_by_prefix(plan_node[0], plan_node[1])
                    self.output_transaction = migration.atomic

                    plan = loader.graph.nodes[plan_node[0], plan_node[1]]
                    sql_statements =executor.collect_sql([(plan, False)])

                    title = plan_node[1]
                    # Mark it as applied/unapplied
                    if plan_node not in loader.applied_migrations:
                        print(f'\033[1;36mApp name: {app_name} - Migration: {title}\033[0;37m')
                        evaluator = SQLStatementsEvaluator(sql_statements)
                        evaluator.evaluate()
