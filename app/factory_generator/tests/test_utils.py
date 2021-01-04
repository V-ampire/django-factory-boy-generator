from django.apps import apps as installed_apps
from django.test import TestCase
from django.core.management.base import CommandError

from factory_generator import utils, FACTORIES_MODULE_NAME

from sample_app import factories as sample_factories
from sample_app import models

from faker import Faker
import os
from unittest.mock import Mock, patch


fake = Faker()


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
        self.app_config = installed_apps.get_app_config('sample_app')
        self.module = sample_factories
    
    def test_get_all_factories(self):
        expected_factories = [
            self.module.CityFactory,
            self.module.CompanyFactory,
            self.module.PersonFactory,
        ]
        tested_factories = utils.get_app_factories(self.app_config)
        expected_factories_names = [utils.get_full_factory_name(f) for f in expected_factories]
        expected_factories_names.sort()
        tested_factories_names = [utils.get_full_factory_name(f) for f in tested_factories]
        tested_factories_names.sort()
        self.assertEqual(
            expected_factories_names,
            tested_factories_names,
        )


    def get_factories_by_names(self):
        expected_factories = [
            self.module.CityFactory,
            self.module.CompanyFactory,
        ]
        tested_factories = utils.get_app_factories(
            self.app_config.path, ['CityFactory', 'CompanyFactory']
        )
        expected_factories_names = [utils.get_full_factory_name(f) for f in expected_factories]
        expected_factories_names.sort()
        tested_factories_names = [utils.get_full_factory_name(f) for f in tested_factories]
        tested_factories_names.sort()
        self.assertEqual(
            expected_factories_names,
            tested_factories_names,
        )

    def test_get_only_django_factories(self):
        tested_factories = utils.get_app_factories(
            self.app_config, ['NotDjangoFactory',]
        )
        self.assertEqual(tested_factories, [])


class TestParseLabels(TestCase):

    def setUp(self):
        self.app_config = installed_apps.get_app_config('sample_app')
        self.module = sample_factories

    def test_with_factory_name(self):
        labels = ['sample_app.CityFactory']
        expected_factories = [
            self.module.CityFactory,
        ] 
        tested_factories = utils.parse_apps_and_factories_labels(labels)
        expected_factories_names = [utils.get_full_factory_name(f) for f in expected_factories]
        expected_factories_names.sort()
        tested_factories_names = [utils.get_full_factory_name(f) for f in tested_factories]
        tested_factories_names.sort()
        self.assertEqual(
            expected_factories_names,
            tested_factories_names,
        )

    def test_with_app_name(self):
        labels = ['sample_app']
        expected_factories = [
            self.module.CityFactory,
            self.module.CompanyFactory,
            self.module.PersonFactory,
        ] 
        tested_factories = utils.parse_apps_and_factories_labels(labels)
        expected_factories_names = [utils.get_full_factory_name(f) for f in expected_factories]
        expected_factories_names.sort()
        tested_factories_names = [utils.get_full_factory_name(f) for f in tested_factories]
        tested_factories_names.sort()
        self.assertEqual(
            expected_factories_names,
            tested_factories_names,
        )

    def test_with_incorrect_label(self):
        expected_msg = 'App or factory specified incorrectly. Use form app_label.FactoryName.'
        labels = ['sample_app.CityFactory.name']
        with self.assertRaises(CommandError) as e:
            execinfo = e
            utils.parse_apps_and_factories_labels(labels)
        self.assertTrue(expected_msg in execinfo.exception.args)

    def test_with_app_not_exists(self):
        invalid_app_name = fake.word()
        expected_msg = f'Unknown app: {invalid_app_name}'
        labels = ['sample_app.CityFactory', invalid_app_name]
        with self.assertRaises(CommandError) as e:
            execinfo = e
            utils.parse_apps_and_factories_labels(labels)
        self.assertTrue(expected_msg in execinfo.exception.args)
    
    def test_with_factory_not_exists(self):
        invalid_factory_name = fake.word()
        expected_msg = f'App sample_app doesnt have {invalid_factory_name} factory'
        labels = [f'sample_app.{invalid_factory_name}']
        with self.assertRaises(CommandError) as e:
            execinfo = e
            utils.parse_apps_and_factories_labels(labels)
        self.assertTrue(expected_msg in execinfo.exception.args)


class TestDeleteByFactory(TestCase):

    def setUp(self):
        self.factory_class = sample_factories.CityFactory
        self.model_class = models.City

    def test_success_delete(self):
        model_instance = self.factory_class.create()
        utils.delete_by_factory(self.factory_class)
        self.assertFalse(self.model_class.objects.all())
    
    def test_success_delete_batch(self):
        self.factory_class.create()
        self.factory_class.create()
        self.factory_class.create()
        result = utils.delete_by_factory(self.factory_class)
        self.assertTrue(self.factory_class._meta.model)
