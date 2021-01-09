from django.test import TestCase

from factory_generator.encoders import DjangoFileJsonEncoder
from factory_generator.generators import generate_to_json
from factory_generator.tests.testapp.factories import PersonFactory

import json
import os


class TestFileJsonEncoder(TestCase):

    def test_encode_files(self):
        encoder = DjangoFileJsonEncoder()
        json_data = generate_to_json(PersonFactory)
        testeded_file_path = json.dumps(os.path.realpath(json_data[0]['passport_scan'].name))
        testeded_image_path = json.dumps(os.path.realpath(json_data[0]['photo'].name))
        expected_file_path = encoder.encode(json_data[0]['passport_scan'])
        expected_image_path = encoder.encode(json_data[0]['photo'])
        
        self.assertEqual(testeded_file_path, expected_file_path)
        self.assertEqual(testeded_image_path, expected_image_path)
        