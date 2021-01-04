from factory_generator.generators import generate_to_json
from factory_generator import utils
from factory_generator.management.base import BaseGenerateCommand


class GenerateToJsonCommand(BaseGenerateCommand):
    help = 'Generate json string using factories in django apps'

    def generate(self, generate_factories, quantity=1):
        json = generate_to_json(generate_factories)
        for i in range(quantity):
            
        self.stdout.write(self.style.SUCCESS(message))
