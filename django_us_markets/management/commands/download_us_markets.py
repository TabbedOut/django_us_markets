from __future__ import print_function

import os
import urllib
from zipfile import ZipFile
from StringIO import StringIO

from csvkit.convert import csv2csv, xls2csv
from django.core.management import BaseCommand

from ...data import make_path
from ...data import ZIP_METADATA, ZIP_SHAPES, MSA_DATA


class Command(BaseCommand):

    help = "Download the raw source data for all US markets"

    def handle(self, *args, **options):
        download_zip_metadata()
        download_zip_shapes()
        download_msa_data()


def download_zip_metadata():
    """
    Download ZIP code metadata from Geonames.

    http://www.geonames.org/
    """
    url = 'http://download.geonames.org/export/zip/US.zip'
    source_path = make_path('geonames')
    download_path = os.path.join(source_path, 'zip_codes.zip')
    raw_text_path = os.path.join(source_path, 'US.txt')
    filename = make_path(ZIP_METADATA)
    print('Downloading {}...'.format(filename))

    urllib.urlretrieve(url, download_path)
    zipfile = ZipFile(download_path)
    zipfile.extractall(source_path)

    with open(raw_text_path) as raw_stream:
        csv_bytes = csv2csv(raw_stream)

    with open(filename, 'w') as csv_stream:
        csv_stream.write(csv_bytes)

    assert os.path.isfile(filename)


def download_msa_data():
    """
    Download MSA data from the Department of Labor OWCP fee schedule.

    This particular dataset (Office of Workers' Compensation Programs)
    is useful because it associates ZIP codes with the MSA belong to.

    http://www.dol.gov/owcp/regs/feeschedule/fee/fee15/download.htm
    """
    url = (
        'http://www.dol.gov/owcp/regs/feeschedule/fee/fee15/'
        'fs15_gpci_by_msa-ZIP.xls'
    )
    download_path = make_path('department_of_labor/owcp_fee_schedule_2015.xls')
    filename = make_path(MSA_DATA)
    print('Downloading {}...'.format(filename))

    urllib.urlretrieve(url, download_path)
    with open(download_path) as xls_stream:
        csv_bytes = xls2csv(xls_stream)
        with open(filename, 'w') as csv_stream:
            # The first 10 lines are junk; ignore them.
            csv_buffer = StringIO(csv_bytes)
            for i, row in enumerate(csv_buffer):
                if i < 10:
                    continue

                csv_stream.write(row)

    assert os.path.isfile(filename)


def download_zip_shapes():
    """
    Download ZIP shapefiles from the US Census TIGERLINE dataset.

    http://www.census.gov/cgi-bin/geo/shapefiles2015/layers.cgi
    """
    url = (
        'ftp://ftp2.census.gov/geo/tiger/TIGER2015/ZCTA5/'
        'tl_2015_us_zcta510.zip'
    )
    source_path = make_path('us_census_bureau')
    download_path = os.path.join(source_path, 'zip_codes_2015.zip')
    filename = make_path(ZIP_SHAPES + '.shp')
    print('Downloading {}...'.format(filename))

    urllib.urlretrieve(url, download_path)
    zipfile = ZipFile(download_path)
    zipfile.extractall(source_path)

    assert os.path.isfile(filename)
