from django.core.serializers.json import DjangoJSONEncoder

import factory
from factory.declarations import SubFactory

import json


def generate_to_dict(factory_class):
    """
    Converting a factory’s output to a dict, including SubFactories
    """
    subs = {}
    factory_data = factory_class.__dict__
    for k in factory_data.keys():
        if isinstance(factory_data[k], SubFactory):
            subs[k] = generate_to_dict(factory_data[k].get_factory())
    return factory.build(dict, FACTORY_CLASS=factory_class, **subs)


def generate_to_json(factory_class, **kwargs):
    """
    Generate json based on factory class.
    """
    if not kwargs.get('cls'):
        kwargs['cls'] = DjangoJSONEncoder
    return json.dumps(generate_to_dict(factory_class), **kwargs)


def generate_to_db(factory_class, quantity=1, **kwargs):
    """
    Generate sample data and fill database.
    """
    return factory_class.create_batch(quantity, **kwargs)

