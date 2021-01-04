# App to generate data for django apps using factories.

## Requirements

- Python 3.6 or newer
- Django >= 2.2 or newer
- factory-boy >= 3.1 or newer

## Features

- Fill database by sample data generated using factories.
- Generate as dict.


## CLI

`python manage.py generate_to_db [app_label[.FactoryName] [app_label[.FactorylName] ...]]`

`--exclude EXCLUDE, -e EXCLUDE`

Prevents specific applications or factories (specified in the form of app_label.FactoryName) from being dumped. If you specify a factory name, the output will be restricted to that factory, rather than the entire application. You can also mix application names and factory names.

If you want to exclude multiple applications, pass --exclude more than once:


`--database DATABASE`

Specifies the database to which data will be generated. Defaults to default.


`--quantity QUANTITY, -q QUANTITY`

Quantity of objects every factory which will be generated.


`--update, -u`

If specified, database will be rewrite. If not, new records will be added.


`-f --file`

Path to configuration *.ini* file related of project base directory.
