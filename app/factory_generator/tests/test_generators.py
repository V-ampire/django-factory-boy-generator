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
        expected_json = [generators.generate_to_dict(CityFactory)]
        result = generators.generate_to_json(CityFactory)
        self.assertEqual(result, expected_json)

    def test_generate_with_quantity(self):
        expected_quantity = 3
        expected_data = [
            generators.generate_to_dict(CityFactory)
            for i in range(expected_quantity)
        ]
        result = generators.generate_to_json(CityFactory, quantity=expected_quantity)
        self.assertEqual(result, expected_data)


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


