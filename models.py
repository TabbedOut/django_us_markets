from django.contrib.gis.db import models
from localflavor.us.models import USStateField


class Community(models.Model):
    """
    A unique name and ID for a community.

    Sourced from Geonames.
    """

    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Market(models.Model):
    """
    An aggregation of metropolitan areas into a major market.

    Based on Metropolitan Statistical Area.
    """

    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class ZIPCode(models.Model):
    """
    Zone Improvement Plan, or United States postal code.
    """

    state = USStateField()
    market = models.ForeignKey(Market)
    community = models.ForeignKey(Community, blank=True, null=True)

    center = models.PointField()
    polygon = models.Polygon()

    def __unicode__(self):
        return unicode(self.id)
