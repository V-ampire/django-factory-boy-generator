from django.core.management import call_command
from django.test import TestCase

from factory_generator.encoders import DjangoFileJsonEncoder
from factory_generator.generators import generate_to_json
from factory_generator.tests.testapp.factories import PersonFactory
from factory_generator.tests.testapp.models import Person

import factory
from io import StringIO
import json
import os
from unittest.mock import patch


class TestRunGenerateToJson(TestCase):
    def call_command(self, *args, **kwargs):
        out = StringIO()
        call_command(
            "generate_to_json",
            *args,
            stdout=out,
            stderr=StringIO(),
            **kwargs,
        )
        return out.getvalue()

    @patch('factory_generator.management.commands.generate_to_json.generate_to_json')
    def test_run_without_options(self, mock_generate):
        expected_fields = generate_to_json(PersonFactory)
        expected_model = 'testapp.person'
        expected_json = json.dumps([{
            'model': expected_model,
            'fields': expected_fields[0]
        }], cls=DjangoFileJsonEncoder)
        mock_generate.return_value = expected_fields
        result_json = self.call_command('testapp.PersonFactory')
        self.assertEqual(result_json, expected_json + '\n')


class TestRunGenerateToDb(TestCase):

    def call_command(self, *args, **kwargs):
        out = StringIO()
        call_command(
            "generate_to_db",
            *args,
            stdout=out,
            stderr=StringIO(),
            **kwargs,
        )
        return out.getvalue()
    
    @patch('factory_generator.management.commands.generate_to_db.generate_to_db')
    def test_run_without_options(self, mock_generate):
        self.call_command('testapp.PersonFactory')
        tested_factory_class = mock_generate.call_args[0][0]
        self.assertEqual(str(tested_factory_class), str(PersonFactory))
        
    