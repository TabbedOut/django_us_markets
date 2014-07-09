Places
======

A Django app for GIS data, including postal codes, metropolitan areas, and community names.


Installation
---

First, check out the repo in `lib/modelo`.

Install any requirements:

    pip install -r requirements.txt

Configure `django.contrib.gis` and install the `places` app:

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
        'places'
    ]

Finally, migrate the app to sync the models to the database:

    python manage.py migrate places



Building the dataset
---

The app can download and build the dataset from primary data.

1. `export PYTHONPATH=.:lib:lib/modelo:lib/site-packages`
2. `export DJANGO_SETTINGS_MODULE=consumer_services.settings.development`
3. `cd lib/modelo/places && make`
4. `cd ../../.. && python lib/modelo/places/load.py`


Example Queries
---

Site users by postal code:

    select u.username, p.postal_code, p.state, m.name as market, c.name as community
    from places_postalcode p
    join device_locatelog l on ST_Contains(p.tabulation, POINT(l.longitude, l.latitude))
    left join profiles_siteuser u on l.user_id = u.id
    left join places_market m on p.market_id = m.id
    left join places_community c on p.community_id = c.id;
