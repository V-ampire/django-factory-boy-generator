from .factory_generator import generators

from .factory_generator.tests.testapp.models import Person, Company

import factory


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    name = factory.Faker('company')
    address = factory.Faker('address')


class PersonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Person

    name = factory.Faker('company')
    phone = factory.Faker('phone_number')
    company = factory.SubFactory(CompanyFactory)


def test_json_generator():
    return generators.generate_to_dict(PersonFactory)

def main():
    print(test_json_generator())

if __name__ == '__main__':
    main()