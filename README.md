Django US Markets
=================

A Django app for GIS data, including postal codes, metropolitan areas, and community names.


Installation
---

Configure `django.contrib.gis` and install the app:

    # settings.py
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.mysql',
            # ...
        }
    }

    INSTALLED_APPS = [
        # ...
        'django.contrib.gis',
        'django_us_markets',
    ]

Finally, migrate the app to sync the models to the database:

    python manage.py migrate places


Building the dataset
---

The app can download and build the dataset from primary data.

  $ cdsitepackages
  $ cd django_us_markets
  $ make
  $ export PYTHONPATH=/my/project
  $ export DJANGO_SETTINGS_MODULE=project.settings
  $ python load.py


Example Queries
---

Venues by postal code:

    SELECT
      v.name,
      p.postal_code,
      p.state,
      m.name as market,
      c.name as community
    FROM venue_venue v
    JOIN django_us_markets_postalcode p
      ON ST_Contains(p.tabulation, POINT(v.longitude, v.latitude))
    LEFT JOIN django_us_markets_market m
      ON p.market_id = m.id
    LEFT JOIN django_us_markets_community c
      ON p.community_id = c.id;
