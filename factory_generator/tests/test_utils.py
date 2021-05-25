from django.apps import apps as installed_apps
from django.test import TestCase
from django.core.management.base import CommandError
from django.conf import settings

from factory_generator import utils

from factory_generator.tests.testapp import factories as sample_factories
from factory_generator.tests.testapp import models

import configparser
from faker import Faker
import os


fake = Faker()

BASE_DIR = settings.BASE_DIR


class TestLoadFileConfig(TestCase):
    
    def setUp(self):
        self.config_path = os.path.join(BASE_DIR, 'factory_generator.ini')
        self.expected_labels = [fake.word() for i in range(3)]
        self.expected_excludes = [fake.word()]
        self.expected_quantity = fake.pyint()
        self.expected_update = fake.boolean()
        config = configparser.ConfigParser()
        config['factory_generator'] = {
            'labels': ','.join(self.expected_labels),
            'exclude': self.expected_excludes[0],
            'quantity': self.expected_quantity,
            'update': self.expected_update
        }
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)

    def tearDown(self):
        os.remove(self.config_path)

    def test_load_config(self):
        config = utils.load_file_config(self.config_path)
        self.assertEqual(config.labels, self.expected_labels)
        self.assertEqual(config.exclude, self.expected_excludes)
        self.assertEqual(config.quantity, self.expected_quantity)
        self.assertEqual(config.update, self.expected_update)

    def test_raise_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            utils.load_file_config(fake.file_path())


class TestGetModule(TestCase):

    def test_import(self):
        expected_module = sample_factories
        file_path = expected_module.__file__
        module_name = expected_module.__name__
        tested_module = utils.get_module(module_name, file_path)
        self.assertEqual(tested_module.__file__, expected_module.__file__)


class TestIsSuper(TestCase):

    def setUp(self):
        """
        ExpectedSuperClass -> ExpectedSubClass -> ExpectedNestedSubClass
        """

        class ExpectedSuperClass():
            pass

        class ExpectedSubClass(ExpectedSuperClass):
            pass

        class ExpectedNestedSubClass(ExpectedSubClass):
            pass

        class InvalidSubClass():
            pass

        self.expected_super_class = ExpectedSuperClass
        self.expected_sub_class = ExpectedSubClass
        self.expected_nested_sub_class = ExpectedNestedSubClass
        self.invalid_sub_class = InvalidSubClass

    def test_return_true(self):
        self.assertTrue(utils.is_super(self.expected_super_class, self.expected_sub_class))
        self.assertTrue(utils.is_super(self.expected_super_class, self.expected_nested_sub_class))

    def test_return_false(self):
        self.assertFalse(utils.is_super(self.expected_super_class, self.invalid_sub_class))
        instance =  self.expected_nested_sub_class()
        # instance doesnt have attribute __bases__
        self.assertFalse(utils.is_super(self.expected_super_class, instance))


class TestGetAppFactories(TestCase):

    def setUp(self):
        self.app_config = installed_apps.get_app_config('testapp')
        self.module = sample_factories
    
    def test_get_app_factories(self):
        expected_factories = [
            self.module.CityFactory,
            self.module.CompanyFactory,
            self.module.PersonFactory,
        ]
        tested_factories = utils.get_app_factories(self.app_config)
        expected_factories.sort(key=str)
        tested_factories.sort(key=str)
        self.assertEqual(
            [str(f) for f in expected_factories],
            [str(f) for f in tested_factories],
        )

    def get_factories_by_names(self):
        expected_factories = [
            self.module.CityFactory,
            self.module.CompanyFactory,
        ]
        tested_factories = utils.get_app_factories(
            self.app_config.path, ['CityFactory', 'CompanyFactory']
        )
        expected_factories.sort(key=str)
        tested_factories.sort(key=str)
        self.assertEqual(
            [str(f) for f in expected_factories],
            [str(f) for f in tested_factories],
        )

    def test_get_only_django_factories(self):
        tested_factories = utils.get_app_factories(
            self.app_config, ['NotDjangoFactory']
        )
        self.assertEqual(tested_factories, [])


class TestParseLabels(TestCase):

    def setUp(self):
        self.app_config = installed_apps.get_app_config('testapp')
        self.module = sample_factories

    def test_with_factory_name(self):
        labels = ['testapp.CityFactory']
        expected_factories = [
            self.module.CityFactory,
        ] 
        tested_factories = utils.parse_factories_from_labels(labels)
        expected_factories.sort(key=str)
        tested_factories.sort(key=str)
        self.assertEqual(
            [str(f) for f in expected_factories],
            [str(f) for f in tested_factories],
        )

    def test_with_app_name(self):
        labels = ['testapp']
        expected_factories = [
            self.module.CityFactory,
            self.module.CompanyFactory,
            self.module.PersonFactory,
        ] 
        tested_factories = utils.parse_factories_from_labels(labels)
        expected_factories.sort(key=str)
        tested_factories.sort(key=str)
        self.assertEqual(
            [str(f) for f in expected_factories],
            [str(f) for f in tested_factories],
        )

    def test_with_incorrect_label(self):
        expected_msg = 'App or factory specified incorrectly. Use form app_label.FactoryName.'
        labels = ['testapp.CityFactory.name']
        with self.assertRaises(CommandError) as e:
            execinfo = e
            utils.parse_factories_from_labels(labels)
        self.assertTrue(expected_msg in execinfo.exception.args)

    def test_with_app_not_exists(self):
        invalid_app_name = fake.word()
        expected_msg = f'Unknown app: {invalid_app_name}'
        labels = ['testapp.CityFactory', invalid_app_name]
        with self.assertRaises(CommandError) as e:
            execinfo = e
            utils.parse_factories_from_labels(labels)
        self.assertTrue(expected_msg in execinfo.exception.args)
    
    def test_with_factory_not_exists(self):
        invalid_factory_name = fake.word()
        expected_msg = f'App testapp doesnt have {invalid_factory_name} factory'
        labels = [f'testapp.{invalid_factory_name}']
        with self.assertRaises(CommandError) as e:
            execinfo = e
            utils.parse_factories_from_labels(labels)
        self.assertTrue(expected_msg in execinfo.exception.args)


class TestDeleteByFactory(TestCase):

    def setUp(self):
        self.factory_class = sample_factories.CityFactory
        self.model_class = models.City

    def test_success_delete(self):
        self.factory_class.create()
        utils.delete_by_factory(self.factory_class)
        self.assertFalse(self.model_class.objects.all())
    
    def test_success_delete_batch(self):
        self.factory_class.create()
        self.factory_class.create()
        self.factory_class.create()
        utils.delete_by_factory(self.factory_class)
        self.assertTrue(self.factory_class._meta.model)
