from django.core.serializers.json import DjangoJSONEncoder

import factory
from factory.declarations import SubFactory

import json


def factory_as_dict(factory_class):
    """
    Converting a factory’s output to a dict, including SubFactories
    """
    subs = {}
    factory_data = factory_class.__dict__
    for k in factory_data.keys():
        if isinstance(factory_data[k], SubFactory):
            subs[k] = generate_to_dict(factory_data[k].get_factory())
    return factory.build(dict, FACTORY_CLASS=factory_class, **subs)


def generate_to_dict(factory_class, quantity=1):
    """
    Generate dict based on factory
    :param quantity: If quantity > 1 return list of dicts. 
    """
    if quantity > 1:
        return [factory_as_dict(factory_class) for i in range(quantity)]
    return factory_as_dict(factory_class)


def generate_to_json(factory_class, quantity=1, **kwargs):
    """
    Generate json based on factory class.
    """
    if not kwargs.get('cls'):
        kwargs['cls'] = DjangoJSONEncoder
    return json.dumps(generate_to_dict(factory_class, quantity=quantity), **kwargs)


def generate_to_db(factory_class, quantity=1, **kwargs):
    """
    Generate sample data and fill database.
    """
    return factory_class.create_batch(**kwargs)

