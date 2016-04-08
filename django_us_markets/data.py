import os


ZIP_METADATA = 'geonames/us_zip_codes.csv'
ZIP_SHAPES = 'us_census_bureau/tl_2015_us_zcta510'
MSA_DATA = 'department_of_labor/owcp_fee_schedule_2015.csv'

DEFAULT_ROOT = os.path.abspath(os.path.join(__file__, '..', 'data'))


def make_path(relative_path, root=DEFAULT_ROOT):
    """
    Get a complete path to a downloaded data file.
    """
    return os.path.join(root, relative_path)
