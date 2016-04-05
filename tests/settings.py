SECRET_KEY = 'foo'

INSTALLED_APPS = ['django_us_markets']

MIDDLEWARE_CLASSES = []

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'django_us_markets',
        'HOST': 'postgis',
        'USER': 'postgres',
        'PASSWORD': 'mysecretpassword',
    },
}
