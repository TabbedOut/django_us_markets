from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin

from . import models


@admin.register(models.PostalCode)
class PostalCodeAdmin(OSMGeoAdmin):

    list_display = ['postal_code', 'community', 'market', 'state', 'country']
    list_filter = ['state']
    raw_id_fields = ['community', 'market']
    search_fields = ['=postal_code']

    def get_queryset(self, request):
        queryset = super(PostalCodeAdmin, self).get_queryset(request)
        return queryset.select_related('community', 'market')


admin.site.register(models.Market)
admin.site.register(models.Community)
