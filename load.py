import collections
import pprint

import csvkit
import shapefile

ZIP_SHP = 'data/us_census_bureau/zip_codes_2013/tl_2013_us_zcta510'
MSA_CSV = 'data/department_of_labor/owcp_fee_schedule_by_zip_2011.csv'
GEO_CSV = 'data/geonames/us_zip_codes.csv'


def read_tabulation_areas():
    reader = shapefile.Reader(ZIP_SHP)
    shapes = reader.iterShapes()
    records = reader.records()

    for record in records:
        shape = next(shapes)
        zip_code, _, _, _, _, _, _, latitude, longitude = record
        yield zip_code, float(latitude), float(longitude), shape


def read_owcp():
    with open(MSA_CSV) as stream:
        reader = csvkit.DictReader(stream)
        for data in reader:
            yield data['ZIP CODE'], data['MSA No.'], data['MSA Name']


def read_geonames():
    with open(GEO_CSV) as stream:
        reader = csvkit.CSVKitReader(stream)
        for row in reader:
            _, zip_code, _, _, state, community_name, community_id = row[:7]
            yield zip_code, state, community_id, community_name


if __name__ == '__main__':
    zip_codes = collections.defaultdict(dict)
    for zip_code, msa_id, msa_name in read_owcp():
        zip_codes[zip_code].update(
            msa_id=msa_id,
            msa_name=msa_name
        )

    for zip_code, state, community_id, community_name in read_geonames():
        zip_codes[zip_code].update(
            state=state,
            community_id=community_id,
            community_name=community_name
        )

    for zip_code, latitude, longitude, shape in read_tabulation_areas():
        zip_codes[zip_code].update(
            latitude=latitude,
            longitude=longitude,
            shape=shape
        )
        print zip_code, ' ',
        pprint.pprint(zip_codes[zip_code])
