import os


ZIP_METADATA = 'geonames/us_zip_codes.csv'
ZIP_SHAPES = 'us_census_bureau/tl_2015_us_zcta510'
MSA_DATA = 'department_of_labor/owcp_fee_schedule_2015.csv'


def make_path(*paths):
    """
    Get a complete path to a downloaded data file.
    """
    relative_path = os.path.join(__file__, '..', 'data')
    absolute_path = os.path.abspath(relative_path)
    return os.path.join(absolute_path, *paths)
