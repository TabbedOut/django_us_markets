import codecs
import collections
import csv
import os

from django.conf import settings
from django.contrib.gis.geos import Point, MultiPolygon, Polygon
from django.contrib.gis.utils import LayerMapping
from django_localflavor_us.forms import USStateField

from places.models import Community, Market, PostalCode


ZIP_SHP = 'data/us_census_bureau/zip_codes_2013/tl_2013_us_zcta510'
MSA_CSV = 'data/department_of_labor/owcp_fee_schedule_by_zip_2011.csv'
GEO_CSV = 'data/geonames/us_zip_codes.csv'


class ZIPCodeMapping(LayerMapping):
    """
    Loads ZIP code shapefiles and associates the resulting models with
    existing place data.
    """
    mapping = {
        'postal_code': 'ZCTA5CE10',
        'tabulation': 'MULTIPOLYGON'
    }

    def __init__(self, model, data, mapping=None, **kwargs):
        kwargs.setdefault('unique', 'postal_code')
        kwargs.setdefault('encoding', 'latin-1')
        mapping = mapping or self.mapping
        self.zip_code_data = dict(kwargs.pop('zip_code_data'))
        super(ZIPCodeMapping, self).__init__(model, data, mapping, **kwargs)

    def feature_kwargs(self, feature):
        kwargs = super(ZIPCodeMapping, self).feature_kwargs(feature)

        latitude = feature['INTPTLAT10'].as_double()
        longitude = feature['INTPTLON10'].as_double()
        center = Point(longitude, latitude)

        number = kwargs['postal_code']
        zip_code = str(number).zfill(5)
        extra_kwargs = self.zip_code_data[zip_code]
        extra_kwargs.pop('latitude', None)
        extra_kwargs.pop('longitude', None)
        extra_kwargs.update(
            id=number,
            center=center,
            postal_code=zip_code,
            country=u'US'
        )

        return dict(kwargs, **extra_kwargs)


def make_path(*paths):
    """
    Get a complete path to a file in the places app.
    """
    return os.path.join(settings.PROJECT_ROOT, 'lib/modelo/places', *paths)


def read_utf8(stream):
    """
    Transform a stream into generator of UTF-8 encoded lines.
    """
    for line in stream:
        yield line.encode('utf-8')


def load_places():
    """
    Reload all places from primary data.
    """
    zip_code_data, community_data, market_data = get_place_data()

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
    zip_shp = make_path(ZIP_SHP + '.shp')
    mapping = ZIPCodeMapping(PostalCode, zip_shp, zip_code_data=zip_code_data)
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


def read_owcp():
    """
    Iterate over the MSA data from the Department of Labor.
    """
    msa_csv = make_path(MSA_CSV)
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


def read_geonames():
    """
    Iterate over the community data from Geonames.
    """
    geo_csv = make_path(GEO_CSV)
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


def get_place_data():
    """
    Get a tuple of `(zip_code_data, community_data, market_data)`.

    Each dataset is a dict mapping IDs to model data.
    """
    zip_code_data = collections.defaultdict(dict)

    for zip_code, owcp_data in read_owcp():
        zip_code_data[zip_code].update(owcp_data)

    for zip_code, geonames_data in read_geonames():
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


if __name__ == '__main__':
    load_places()
