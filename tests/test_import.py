import os

from django.core.management import call_command
from django.test import TestCase

from django_us_markets.models import PostalCode


class ImportTestCase(TestCase):

    def test_import_imports_data_from_specified_path(self):
        directory = os.path.dirname(__file__)
        fixtures_path = os.path.join(directory, 'fixtures')
        call_command('load_us_markets', data_path=fixtures_path)

        postal_code = PostalCode.objects.get(postal_code='78404')
        self.assertEqual(str(postal_code.market), 'Corpus Christi, TX MSA')
        self.assertEqual(str(postal_code.community), 'Nueces')

        postal_code = PostalCode.objects.get(postal_code='78704')
        self.assertEqual(str(postal_code.market), 'Austin-Round Rock, TX MSA')
        self.assertEqual(str(postal_code.community), 'Travis')
