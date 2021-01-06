from django.core.serializers.json import DjangoJSONEncoder

from factory_generator.generators import generate_to_json
from factory_generator.management.base import BaseGenerateCommand

import json


class Command(BaseGenerateCommand):
    help = 'Generate json string using factories in django apps'

    def generate(self, generate_factories, update=False, quantity=1, **kwargs):
        """
        Return json string contains models label and fiels as dict representation of factory class.
        For json serializing uses DjangoJSONEncoder as default, to specify encoder pass kwarg cls.
        """
        if not kwargs.get('cls'):
            kwargs['cls'] = DjangoJSONEncoder

        result = []
        for factory_class in generate_factories:
            model_label = factory_class._meta.model._meta.label_lower
            factories_data = generate_to_json(factory_class, quantity=quantity)
            for factory_data in factories_data:
                result.append(
                    {
                        'model': model_label,
                        'fields': factory_data
                    }
                )
        return json.dumps(result, **kwargs)
