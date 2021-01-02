from sample_app.models import Company, Person, City

import factory
from faker import Faker

from datetime import datetime

f = Faker()


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City
    name = f.city()


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company
    name = f.company()
    address = f.address()
    city = factory.SubFactory(CityFactory)


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Person

    name = f.first_name()
    phone = factory.Sequence(lambda n: '123-555-%04d' % n)
    company = factory.SubFactory(CompanyFactory)
    timestamp = factory.LazyFunction(datetime.now)
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.name)


class NotDjangoFactory(factory.Factory):
    class Meta:
        model = City
    name = f.city()