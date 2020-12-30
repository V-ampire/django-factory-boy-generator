class IncorrectFactoryClassError(Exception):
    def __init__(self, message=None):
        msg = 'Factory must be subclass of factory.django.DjangoModelFactory'
        self.message = message if message else msg