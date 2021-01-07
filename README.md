# App to generate data for django apps using [factory-boy](https://github.com/FactoryBoy/factory_boy) factories.


## Table of contents
- [Requirements](#requirements)
- [Installation](#install)
- [Usage](#usage)
- [Configuration from file](#config)
- [Advanced usege](#advanced)


<a name="install"></a>
## Installation

`pip install django-factory-boy-generator`

Add `factory_generator` to your `INSTALLED_APPS` setting.
```
INSTALLED_APPS = [
    ...
    'factory_generator',
]
```


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

### Use django-admin commands:

- Generate records in database:

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


### Use generators as functions.

**django-factory-boy-generator** provides 3 generators:

- `generate_to_dict(factory_class)`

Converting a factory’s output to a dict, including SubFactories.


- `generate_to_json(factory_class, quantity=1, **kwargs)`

Generate json data based on factory class.Return list of dictionaries with generated data.


- `generate_to_db(factory_class, quantity=1, **kwargs)`

Generate sample data and use it to fill database.


You also can use generators, for example, in unit tests:
```
from django.test import TestCase
from factory_generator import generate_to_db, generate_to_db
from sample_app.factories import PersonFactory


class TestSomeActions(TestCase):

    def setUp(self):
        self.persons = generate_to_db(PersonFactory, quantity=5)
        self.persons_data = generate_to_json(PersonFactory, quantity=5)

    ...  # your tests
```


<a name="config"></a>
## Configuration from file

Instead of to pass options every time into command line, you can create `.ini` file with options, which will be used every time when you run commands:
```
[factory_generator]
labels=sample_app, another_app.SomeFactory
exclude=another_app.DontGenerateFactory
quantity=3
update=on
```


<a name="advanced"></a>
## Advanced usage

By default, `generate_to_json` command uses DjangoJSONEncoder. If you want to use another json encoder you can create your custon command extends `factory_generator.management.commands.generate_to_json.Command` and specify encoder pass keyword argument `cls` like this:
```
# your_app.management.commands.create_json

from factory_generator.management.commands.generate_to_json import Command as JsonCommand
from your_app.serializers import CustomJsonEncoder

class Command(JsonCommand):

    def generate(self, generate_factories, quantity=1, **kwargs)
        return super().generate(generate_factories, quantity=1, cls=CustomJsonEncoder)
```
