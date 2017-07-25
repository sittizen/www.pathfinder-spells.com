from importlib import import_module

import yaml
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = ''

    def add_arguments(self, parser):
        parser.add_argument('file')

    def handle(self, *args, **options):
        with open(options['file']) as f:
            data = yaml.load(f)
            importer_path, importer_fun = data['importer'].split('.')
            importer_package = import_module("%s.importer" % importer_path)
            getattr(importer_package, importer_fun)(data)

        self.stdout.write(self.style.SUCCESS('Done'))
