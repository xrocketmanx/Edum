from django.conf.urls import patterns, url, include
from django.contrib import admin

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
    url(r'^', include('app.urls')),
    url(r'^editor/', include('editor.urls')),
    url(r'^users/', include('usersys.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
