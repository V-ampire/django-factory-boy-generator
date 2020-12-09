import factory


class CompanyFactory(factory.django.DjangoModelFactory):
    """
    Фабрика для модели компании.
    """
    class Meta:
        model = models.Company

    user = factory.SubFactory(accounts_factories.CompanyUserAccountModelFactory)
    title = factory.Faker('company')
    inn = factory.Faker('pystr', max_chars=12)
    ogrn = factory.Faker('pystr', max_chars=15)
    city = factory.Faker('city')
    address = factory.Faker('address')
    email = factory.Faker('company_email')
    phone = factory.Faker('phone_number')
    logo = factory.django.ImageField(filename=fake.file_name(extension='jpg'))
    tagline = factory.Faker('catch_phrase')
