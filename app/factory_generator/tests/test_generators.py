from django.test import TestCase

import json

from factory_generator import generators

from sample_app.factories import CompanyFactory, PersonFactory


class TestDictGenerator(TestCase):
    
    def test_generate(self):
        result = generators.generate_to_dict(PersonFactory)
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(isinstance(result['company'], dict))
        self.assertTrue(isinstance(result['company']['city'], dict))


# class TestJsonGenerator(TestCase):

#     def test_generate(self):
#         result = generators.generate_to_json(PersonFactory)
#         print(result)
#         self.assertEqual(json.dumps(generators.generate_to_dict(PersonFactory)), result)
