import tempfile

DEBUG = True

SECRET_KEY = 'foo'

INSTALLED_APPS = [
    'django_us_markets',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.gis',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'tests.urls'

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

STATIC_ROOT = tempfile.mkdtemp()

STATIC_URL = '/static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'django_us_markets',
        'HOST': 'postgis',
        'USER': 'postgres',
        'PASSWORD': 'mysecretpassword',
    },
}
