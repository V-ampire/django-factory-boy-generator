import factory
from factory.declarations import SubFactory
from typing import Dict, List


def generate_to_dict(factory_class) -> Dict:
    """
    Converting a factory’s output to a dict, including SubFactories
    """
    subs = {}
    factory_data = factory_class.__dict__
    for k in factory_data.keys():
        if isinstance(factory_data[k], SubFactory):
            subs[k] = generate_to_dict(factory_data[k].get_factory())
    return factory.build(dict, FACTORY_CLASS=factory_class, **subs)


def generate_to_json(factory_class, quantity=1, **kwargs) -> List[Dict]:
    """
    Generate json data based on factory class.
    Return list of dictionaries with generated data.
    """
    json_data = []
    for i in range(quantity):
        json_data.append(generate_to_dict(factory_class))
    return json_data


def generate_to_db(factory_class, quantity=1, **kwargs):
    """
    Generate sample data and fill database.
    """
    return factory_class.create_batch(quantity, **kwargs)
