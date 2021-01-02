from django.apps import apps as installed_apps
from django.conf import settings
from django.core.management.base import CommandError

import configparser
from factory.django import DjangoModelFactory
import importlib
import os
import sys
from typing import NamedTuple, List, Optional

from . import FACTORIES_MODULE_NAME

BASE_DIR = settings.BASE_DIR


class Config(NamedTuple):
    apps: List[str]
    quantity: int


def get_config_path() -> str:
    return os.path.join(BASE_DIR, 'factory_generator.ini')


def load_file_config() -> Config:
    """
    Return Config object
    """
    config = configparser.ConfigParser()
    config.read(get_config_path())
    apps = config['factory_generator']['apps'].split(sep=',')
    quantity = int(config['factory_generator']['quantity'])
    return Config(apps=apps, quantity=quantity)


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


def is_super(cls, obj):
    """
    Return True if cls is superclass for obj, else return False.
    """
    try:
        if cls in obj.__bases__:
            return True
        for supercls in obj.__bases__:
            return is_super(cls, supercls)
    except AttributeError:
        return False


def get_app_factories(app_path: str, factories_names: List[str]=[]) -> List[DjangoModelFactory]:
    """
    Return list of instances of DjangoModelFactory.
    :param app: Filesystem path to the django application directory.
    :param factories_names: List of names of concrete factories to get.

    Raise AttributeError if factory module doesnt have specified factory.
    """
    factories = set()
    module_name = FACTORIES_MODULE_NAME
    file_path = os.path.join(app_path, f'{FACTORIES_MODULE_NAME}.py')
    factory_module = get_module(module_name, file_path)
    module_objects = factories_names if factories_names else dir(factory_module)
    for obj_name in module_objects:
        obj = getattr(factory_module, obj_name)
        if is_super(DjangoModelFactory, obj):
            factories.add(obj)
    return list(factories)


def parse_apps_and_factories_labels(labels: List[str]) -> List[DjangoModelFactory]:
    """
    Parse a list of "app_label.FactoryName" or "app_label" strings into actual
    objects and return a list of instances of DjangoModelFactory
    Raise a CommandError if some specified factory or apps don't exist.
    """
    factories = set()
    for label in labels:
        if '.' in label:
            try:
                app_name, factory_name = label.split('.')
                app_config = installed_apps.get_app_config(app_name)
            except ValueError:
                raise CommandError('App or factory specified incorrectly. Use form app_label.FactoryName.')
            
            except LookupError as e:
                raise CommandError(f'Unknown factory: {label}')

            try:
                factories.update(get_app_factories(app_config.path, [factory_name]))
            except AttributeError:
                raise CommandError(f'App {app_name} doesnt have {factory_name} factory')
        
        else:
            try:
                app_config = installed_apps.get_app_config(label)
            except LookupError as e:
                raise CommandError(f'Unknown app: {label}')
            factories.update(get_app_factories(app_config.path))
    return list(factories)







    

