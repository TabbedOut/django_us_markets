from django.contrib.gis.db import models


class Community(models.Model):
    """
    A unique name and ID for a community.

    Sourced from Geonames.
    """

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Market(models.Model):
    """
    An aggregation of metropolitan areas into a major market.

    Based on Metropolitan Statistical Area.
    """

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class PostalCode(models.Model):
    """
    A postal code representing a general location.

    Shapes are sourced from ZIP code tabulation area data provided by
    the US Census Bureau.
    """

    postal_code = models.CharField(max_length=7, unique=True)
    state = models.SlugField(max_length=255)
    country = models.SlugField(max_length=2, help_text='ISO 3166-1 alpha-2')
    market = models.ForeignKey(
        to=Market,
        blank=True, null=True,
        related_name='postal_codes'
    )
    community = models.ForeignKey(
        to=Community,
        blank=True, null=True,
        related_name='postal_codes'
    )

    center = models.PointField(db_index=False)
    tabulation = models.MultiPolygonField(db_index=False)

    def __unicode__(self):
        return self.postal_code
