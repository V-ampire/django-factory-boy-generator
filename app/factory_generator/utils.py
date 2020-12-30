
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
from .exceptions import IncorrectFactoryClassError

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


def get_module(file_path: str, module_name: str=FACTORIES_MODULE_NAME):
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


def parse_apps_and_factories_labels(labels: List[str]) -> List[DjangoModelFactory]:
    """
    Parse a list of "app_label.FactoryName" or "app_label" strings into actual
    objects and return a list of instances of DjangoModelFactory
    Raise a CommandError if some specified factory or apps don't exist.
    """
    factories = []
    for label in labels:
        if '.' in label:
            try:
                app_name, factory_name = label.split('.')
            except ValueError:
                raise CommandError('App or factory specified incorrectly. Use form app_label.FactoryName.')
            try:
                app_config = installed_apps.get_app_config(app_name)
            except LookupError as e:
                raise CommandError(f'Unknown factory: {label}')
            factory_module = get_module(app_config.path)
            try:
                getattr(factory_module, factory_name)
            except AttributeError:
                raise CommandError(f'App {app_name} doesnt have {factory_name} factory')







def get_factory_from_app(app_label: str, factory_name: str) -> DjangoModelFactory:
    """
    Return the factory matching the given app_label and factory_name.

    Raise LookupError if no application exists with this label, or no
    factory exists with this name in the application.
    """
    app_config = installed_apps.get_app_config(app_label)
    file_path = os.path.join(app_config.path, f'{FACTORIES_MODULE_NAME}.py')
    factory_module = get_module(FACTORIES_MODULE_NAME, file_path)
    factory_class = getattr(factory_module, factory_name)






    

def get_app_factories(app_path: str) -> List[DjangoModelFactory]:
    """
    Return list of instances of DjangoModelFactory.
    :param app: Filesystem path to the django application directory.
    """
    factories = set()
    module_name = FACTORIES_MODULE_NAME
    file_path = os.path.join(app_path, f'{FACTORIES_MODULE_NAME}.py')
    factory_module = get_module(module_name, file_path)
    for obj_name in dir(factory_module):
        obj = getattr(factory_module, obj_name)
        try:
            if DjangoModelFactory in obj.__bases__:
                factories.append(obj)
        except AttributeError:
            # If object has no attribute '__bases__'
            pass
    return factories