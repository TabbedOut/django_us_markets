from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),
]
