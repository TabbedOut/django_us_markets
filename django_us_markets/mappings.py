from django.contrib.gis.utils import LayerMapping

from django.contrib.gis.geos import Point


class PostalCodeMapping(LayerMapping):
    """
    Loads ZIP code shapefiles from TIGER ZCTA5 postal code data.

    Associates the resulting models with existing place data.
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
        super(PostalCodeMapping, self).__init__(model, data, mapping, **kwargs)

    def feature_kwargs(self, feature):
        kwargs = super(PostalCodeMapping, self).feature_kwargs(feature)

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
