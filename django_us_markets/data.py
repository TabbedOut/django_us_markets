import os


ZIP_METADATA = 'geonames/us_zip_codes.csv'
ZIP_SHAPES = 'us_census_bureau/tl_2015_us_zcta510'
MSA_DATA = 'department_of_labor/owcp_fee_schedule_2015.csv'

APP_ROOT = os.path.abspath(os.path.dirname(__file__))
DEFAULT_ROOT = os.path.join(APP_ROOT, 'data')


def make_path(relative_path, root=None):
    """
    Get a complete path to a downloaded data file.
    """
    root = root or DEFAULT_ROOT
    return os.path.join(root, relative_path)
