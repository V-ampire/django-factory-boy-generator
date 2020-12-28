from django.conf import settings

import configparser
from factory.django import DjangoModelFactory
import importlib
import os
import sys
from typing import NamedTuple, List


BASE_DIR = settings.BASE_DIR
FACTORIES_MODULE_NAME = 'factories'


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
    

def get_app_factories(app_path: str) -> List[DjangoModelFactory]:
    """
    Return list of instances of DjangoModelFactory.
    :param app: Filesystem path to the django application directory.
    """
    factories = []
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