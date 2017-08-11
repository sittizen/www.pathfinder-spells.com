import json
import yaml

from django.core.management.base import BaseCommand

from pathfinder_spells.spelltables.importer import YamlSpell


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('input')
        parser.add_argument('output')

    def handle(self, *args, **options):
        with open(options['input']) as input, open(options['output'], 'w') as output:
            output.write('importer: spelltables.spells\n\n')
            output.write(yaml.dump({'objects': [YamlSpell(**spell) for spell in json.loads(input.read())]}))

        self.stdout.write(self.style.SUCCESS('Done'))
