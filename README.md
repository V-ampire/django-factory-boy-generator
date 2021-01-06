# App to generate data for django apps using [factory-boy](https://github.com/FactoryBoy/factory_boy) factories.

## Table of contents
- [Requirements](#requirements)
- [Usage](#usage)
- [Configuration from file](#config)


<a name="requirements"></a>
## Requirements

- Python 3.6 or newer
- Django >= 1.11 or newer
- factory-boy >= 3.2 or newer


<a name="usage"></a>
## Usage

1. Create in your django app(s) module `factories.py`.
2. Define in this module factories according to [factory-boy docs](https://factoryboy.readthedocs.io/en/stable/orms.html).
All factories for a Django Model should use the DjangoModelFactory base class.

Example:
```
# sample_app/models.py
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=64)
    phone = models.CharField(max_length=12)
    email = models.CharField(max_length=64)


# sample_app/factories.py

from sample_app.models import Person
import factory

class PersonFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('first_name')
    phone = factory.Sequence(lambda n: '123-555-%04d' % n)
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.name)
```

3. Use django-admin commands:

- Generae records in database:

`python manage.py generate_to_db [app_label[.FactoryName] [app_label[.FactorylName] ...]]`


- Generate data to json:

`python manage.py generate_to_json [app_label[.FactoryName] [app_label[.FactorylName] ...]]`


Options:

`--exclude EXCLUDE, -e EXCLUDE`

Prevents specific applications or factories (specified in the form of app_label.FactoryName) from being generated. If you specify a factory name, the result will be restricted to that factory, rather than the entire application. You can also mix application names and factory names.

If you want to exclude multiple applications, pass --exclude more than once:


`--quantity QUANTITY, -q QUANTITY`

Quantity of objects every factory which will be generated.


`--update, -u`

If specified, database will be rewrite. If not, new records will be added.


`-f --file`

Path to configuration *.ini* file related of project base directory. See [configuration from file](#config)


4. Use generators as functions.

*django-factory-boy-generator* provides 3 generators:

- `generate_to_dict(factory_class)`

Converting a factory’s output to a dict, including SubFactories.


- `generate_to_json(factory_class, quantity=1, **kwargs)`

Generate json data based on factory class.Return list of dictionaries with generated data.


- `generate_to_db(factory_class, quantity=1, **kwargs)`

Generate sample data and use it to fill database.


You also can use generators, for example, in unit tests:
```
from django.test import TestCase
from factory_generator import generate_to_db
from sample_app.factories import PersonFactory


class TestSomeActionsWithDb(TestCase):

    def setUp(self):
        self.persons = generate_to_db(PersonFactory, quantity=5)

    ...  # your tests
```
