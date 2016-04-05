from django.core.management import call_command
from django.test import TestCase


class ImportTestCase(TestCase):

    def test_import_imports_all_data(self):
        call_command('load_us_markets')
