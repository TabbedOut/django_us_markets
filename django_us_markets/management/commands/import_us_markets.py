import codecs
import collections
import csv
from optparse import make_option

from django.contrib.gis.geos import Point, MultiPolygon, Polygon
from django.core.management import BaseCommand
from django_us_markets.models import Community, Market, PostalCode
from django_us_markets.mappings import PostalCodeMapping

from ...data import make_path
from ...data import ZIP_METADATA, ZIP_SHAPES, MSA_DATA


ZIP_SHAPEFILE = ZIP_SHAPES + '.shp'


class Command(BaseCommand):

    help = "Delete and reload all US markets from source data"

    option_list = BaseCommand.option_list + (
        make_option('-d', '--data_path', action='store', dest='data_path',
                    default=None, help='A custom path to the source data.'),
    )

    def handle(self, *args, **options):
        root = options['data_path']
        reload_places(root)


# Helpers
#########

def reload_places(root=None):
    """
    Reload all places from primary data.
    """
    zip_code_data, community_data, market_data = get_place_data(root)

    # Reload all communities
    Community.objects.all().delete()
    Community.objects.bulk_create([
        Community(id=id, name=name)
        for id, name in community_data.iteritems()
    ])

    # Reload all markets
    Market.objects.all().delete()
    Market.objects.bulk_create([
        Market(id=id, name=name)
        for id, name in market_data.iteritems()
    ])

    # Reload all ZIP codes
    PostalCode.objects.all().delete()
    zip_shp = make_path(ZIP_SHAPEFILE, root=root)
    mapping = PostalCodeMapping(
        model=PostalCode,
        data=zip_shp,
        zip_code_data=zip_code_data
    )
    mapping.save()

    # Create any ZIP codes that were missing from the Census tabulation.
    # MySQL can't index nullable geometry columns so we insert them with
    # empty tabulations and (0.0, 0.0) centers where necessary.
    polygon = Polygon.from_bbox(((0, 0, 0, 0)))
    tabulation = MultiPolygon(polygon)
    postal_codes = PostalCode.objects.all()
    all_zip_codes = set(postal_codes.values_list('postal_code', flat=True))
    for zip_code, data in zip_code_data.iteritems():
        data.setdefault('latitude', 0.0)
        data.setdefault('longitude', 0.0)
        if zip_code not in all_zip_codes:
            PostalCode.objects.create(
                id=int(zip_code),
                postal_code=zip_code,
                market_id=data['market_id'],
                community_id=data['community_id'],
                center=Point(data['longitude'], data['latitude']),
                tabulation=tabulation,
                state=data['state'],
                country='US'
            )


def get_place_data(root):
    """
    Get a tuple of `(zip_code_data, community_data, market_data)`.

    Each dataset is a dict mapping IDs to model data.
    """
    zip_code_data = collections.defaultdict(dict)

    for zip_code, owcp_data in read_owcp(root):
        zip_code_data[zip_code].update(owcp_data)

    for zip_code, geonames_data in read_geonames(root):
        zip_code_data[zip_code].update(geonames_data)

    community_data, market_data = dict(), dict()
    for zip_code, data in zip_code_data.iteritems():
        community_id = data.pop('community_id', None)
        community_name = data.pop('community_name', None) or 'N/A'
        if community_id:
            community_id = int(float(community_id))
            community_data.setdefault(community_id, community_name)

        msa_id = data.pop('msa_id', None)
        msa_name = data.pop('msa_name', None) or 'N/A'
        if msa_id:
            msa_id = int(float(msa_id))
            market_data.setdefault(msa_id, msa_name)

        data.update(community_id=community_id, market_id=msa_id)

    return zip_code_data, community_data, market_data


def read_owcp(root):
    """
    Iterate over the MSA data from the Department of Labor.
    """
    msa_csv = make_path(MSA_DATA, root=root)
    with codecs.open(msa_csv, 'r', encoding='iso-8859-1') as stream:
        utf8_stream = read_utf8(stream)
        reader = csv.DictReader(utf8_stream)
        for data in reader:
            zip_code = str(int(float(data['ZIP CODE']))).zfill(5)
            yield zip_code, dict(
                msa_id=data['MSA No.'],
                msa_name=data['MSA Name'],
                state=data['STATE']
            )


def read_geonames(root):
    """
    Iterate over the community data from Geonames.
    """
    geo_csv = make_path(ZIP_METADATA, root=root)
    with codecs.open(geo_csv, 'r', encoding='iso-8859-1') as stream:
        utf8_stream = read_utf8(stream)
        reader = csv.reader(utf8_stream)
        for row in reader:
            (_, zip_code, _, _, state, community_name, community_id,
             _, _, latitude, longitude) = row[:11]
            yield zip_code, dict(
                state=state,
                community_id=community_id,
                community_name=community_name,
                latitude=float(latitude),
                longitude=float(longitude)
            )


def read_utf8(stream):
    """
    Transform a stream into generator of UTF-8 encoded lines.
    """
    for line in stream:
        yield line.encode('utf-8')
