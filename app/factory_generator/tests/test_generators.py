from django.core.serializers.json import DjangoJSONEncoder
from django.test import TestCase
from django.utils import timezone

from datetime import datetime
import json
from unittest.mock import patch, Mock

from factory_generator import generators

from sample_app.factories import CompanyFactory, PersonFactory, CityFactory


class TestDictGenerator(TestCase):
    
    def test_generate(self):
        result = generators.generate_to_dict(PersonFactory)
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(isinstance(result['company'], dict))
        self.assertTrue(isinstance(result['company']['city'], dict))


class TestJsonGenerator(TestCase):

    def test_generate(self):
        expected_json = json.dumps(generators.generate_to_dict(CityFactory), 
                                    cls=DjangoJSONEncoder)
        result = generators.generate_to_json(CityFactory)
        self.assertEqual(result, expected_json)

    @patch('factory_generator.generators.json.dumps')
    def test_default_encoder(self, mock_dumps):
        generators.generate_to_json(PersonFactory)
        self.assertEqual(mock_dumps.call_args.kwargs['cls'], DjangoJSONEncoder)


class TestDbGenerator(TestCase):

    @patch.object(CompanyFactory, 'create_batch')
    def test_call_create_batch(self, mock_create):
        expected_quantity = 1
        generators.generate_to_db(CompanyFactory)
        mock_create.assert_called_once()
        mock_create.assert_called_with(expected_quantity)

    @patch.object(CompanyFactory, 'create_batch')
    def test_call_create_batch(self, mock_create):
        expected_quantity = 3
        generators.generate_to_db(CompanyFactory, quantity=expected_quantity)
        mock_create.assert_called_once()
        mock_create.assert_called_with(expected_quantity)


