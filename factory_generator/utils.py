from django.apps import apps as installed_apps
from django.apps import AppConfig
from django.conf import settings
from django.core.management.base import CommandError

import configparser
from factory.django import DjangoModelFactory
import importlib
import logging
import os
import sys
from typing import NamedTuple, List, Dict, Tuple

from factory_generator import FACTORIES_MODULE_NAME


logger = logging.getLogger(__name__)

BASE_DIR = settings.BASE_DIR


class Config(NamedTuple):
    """
    Configuration object.
    :attr labels: Restricts generated data to the specified app_label or app_label.FactoryName. 
    :attr quantity: Quantity of inctances of each factory which will be generate.
    :attr exclude: An app_label or app_label.FactoryName to exclude.
    :attr update: If specified, database will be rewrite. If not, new records will be added.
    """
    labels: List[str]
    quantity: int
    exclude: List[str]
    update: bool


def get_full_file_path(file_path: str) -> str:
    return os.path.join(BASE_DIR, file_path)


def load_file_config(config_path: str) -> Config:
    """
    Return Config object.
    :param config_path: Path to configuration .ini file.

    Raise FileNotFoundError in config file not found.
    """
    config = configparser.ConfigParser()
    with open(config_path, 'r') as fp:
        config.read_file(fp)

    try:
        labels = config['factory_generator']['labels'].split(sep=',')
    except KeyError:
        labels = []

    try:
        exclude = config['factory_generator']['exclude'].split(sep=',')
    except KeyError:
        exclude = []

    quantity = int(config['factory_generator'].get('quantity', 1))
    update = bool(config['factory_generator'].getboolean('update'))
    return Config(labels=labels, quantity=quantity, exclude=exclude, update=update)


def get_module(module_name: str, file_path: str):
    """
    Import and return module.
    :param module_name: Name of module.
    :param file_path: Path to module file.
    """
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def is_super(supercls, obj) -> bool:
    """
    Return True if supercls is superclass for obj, else return False.
    """
    try:
        if supercls in obj.__bases__:
            return True
        for cls in obj.__bases__:
            return is_super(supercls, cls)
    except AttributeError:
        return False


def get_app_factories(app_config: AppConfig, factories_names: List[str]=[]) -> List[DjangoModelFactory]:
    """
    Return list of instances of DjangoModelFactory in app.
    :param app_config: Django application config object.
    :param factories_names: List of names of concrete factories to get.

    Raise AttributeError if factory module doesnt have specified factory.
    """
    factories = set()
    module_name = f'{app_config.name}.{FACTORIES_MODULE_NAME}'
    file_path = os.path.join(app_config.path, f'{FACTORIES_MODULE_NAME}.py')
    try:
        factory_module = get_module(module_name, file_path)
    except FileNotFoundError:
        logger.debug(f'Factory module {module_name} not found.')
        return list(factories)
    module_objects = factories_names if factories_names else dir(factory_module)
    for obj_name in module_objects:
        obj = getattr(factory_module, obj_name)
        if is_super(DjangoModelFactory, obj):
            factories.add(obj)
    return list(factories)


def get_all_factories() -> List[DjangoModelFactory]:
    """
    Return factory classes from each app.
    """
    factories = set()
    for app_config in installed_apps.get_app_configs():
        factories.update(get_app_factories(app_config))
    return list(factories)


def parse_factories_from_labels(labels: List[str], exclude: List[str]=[]) -> List[DjangoModelFactory]:
    """
    Parse a labels of "app_label.FactoryName" or "app_label" and exclude it if it's nessesary.
    :param labels: List of labels of "app_label.FactoryName" or "app_label".
    :param exclude: List of labels to exclude.

    Returns a list of subclasses DjangoModelFactory
    """
    factories = set()

    for label in labels:
        if label not in exclude:
            if '.' in label:
                try:
                    app_name, factory_name = label.split('.')
                except ValueError:
                    raise CommandError('App or factory specified incorrectly. Use form app_label.FactoryName.')

                if app_name not in exclude:
                    try:
                        app_config = installed_apps.get_app_config(app_name)
                    except LookupError:
                        raise CommandError(f'Unknown app: {app_name}')

                    try:
                        factories.update(get_app_factories(app_config, [factory_name]))
                    except AttributeError:
                        raise CommandError(f'App {app_name} doesnt have {factory_name} factory')
            
            else:
                try:
                    app_config = installed_apps.get_app_config(label)
                except LookupError:
                    raise CommandError(f'Unknown app: {label}')
                factories.update(get_app_factories(app_config))
    return list(factories)


def delete_by_factory(factory_class: DjangoModelFactory) -> Dict:
    """
    Delete all instances of model of DjangoModelFactory.
    :param factory_class: Class inherits from DjangoModelFactory.
    """
    if not is_super(DjangoModelFactory, factory_class):
        raise TypeError('Factory class must be subclass of factory.django.DjangoModelFactory')
    
    model_class = factory_class._meta.get_model_class()
    return model_class.objects.all().delete()