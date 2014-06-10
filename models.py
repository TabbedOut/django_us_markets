from django.contrib.gis.db import models
from django_localflavor_us.models import USStateField


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


class ZIPCode(models.Model):
    """
    Zone Improvement Plan, or United States postal code.

    Shapes are sourced from ZIP code tabulation area data provided by
    the US Census Bureau.
    """

    id = models.IntegerField(primary_key=True)
    state = USStateField()
    market = models.ForeignKey(
        to=Market,
        blank=True, null=True,
        related_name='zip_codes'
    )
    community = models.ForeignKey(
        to=Community,
        blank=True, null=True,
        related_name='zip_codes'
    )

    center = models.PointField(db_index=False)
    tabulation = models.MultiPolygonField(db_index=False)

    def __unicode__(self):
        return unicode(self.id)
