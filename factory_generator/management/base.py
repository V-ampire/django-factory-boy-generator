from django.apps import apps as installed_apps
from django.core.management.base import BaseCommand, CommandError

from factory.django import DjangoModelFactory
from typing import List

from factory_generator import utils


class BaseGenerateCommand(BaseCommand):
    """
    Base class for generating commands.
    It defines getting options and parameters for generating.
    """
    def generate(self, generate_factories: List[DjangoModelFactory], 
                    update=False, quantity=1, **kwargs):
        raise NotImplementedError('You should define method to generate.')

    def add_arguments(self, parser):
        parser.add_argument(
            'args', metavar='app_label[.FactoryName]', nargs='*',
            help='Restricts generated data to the specified app_label or app_label.FactoryName.',
        )

        parser.add_argument(
            '-e', '--exclude', action='append', default=[],
            help='An app_label or app_label.FactoryName to exclude '
                 '(use multiple --exclude to exclude multiple apps/factories).',
        )

        parser.add_argument(
            '-q', '--quantity', type=int, default=1, nargs='?',
            help='Quantity of inctances of each factory which will be generate.',
        )

        parser.add_argument(
            '-u', '--update', action='store_true',
            help='If specified, database will be rewrite. If not, new records will be added.',
        )

        parser.add_argument(
            '-f', '--file', type=str,
            help='Path to configuration .ini file related of project base directory.',
        )

    def handle(self, *args, **options):
        if options['file']:
            config_path = utils.get_full_file_path(options['file'])
            try:
                config = utils.load_file_config(config_path)
                excludes = config.exclude
                quantity = config.quantity
                update = config.update
                labels = config.labels
            except FileNotFoundError:
                raise CommandError(f'Configuration file {config_path} not found.')
        else:
            excludes = options['exclude']
            quantity = options['quantity']
            update = options['update']
            labels = args
            
        generate_factories = []

        if not labels:
            for app_config in installed_apps.get_app_configs():
                generate_factories.extend(utils.get_app_factories(app_config))
        else:
            generate_factories.extend(utils.parse_apps_and_factories_labels(labels))
        
        if excludes:
            exclude_factories_list = utils.parse_apps_and_factories_labels(excludes)
            generate_factories = utils.exclude_factories(generate_factories, exclude_factories_list)

        return self.generate(generate_factories, update=update, quantity=quantity)
