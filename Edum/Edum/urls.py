"""
Definition of urls for Edum.
"""

from datetime import datetime
from django.conf.urls import patterns, url, include
from django.contrib import admin
from app.forms import BootstrapAuthenticationForm

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.home', name='home'),
    url(r'^contact$', 'app.views.contact', name='contact'),
    url(r'^about', 'app.views.about', name='about'),
    url(r'^courses$', 'app.views.courses', name='courses'),
    url(r'^courses/add_course$', 'app.views.add_course', name='add_course'),
    url(r'^courses/(?P<course_id>\d+)$', 'app.views.course', name='course'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)$', 'app.views.module', name='module'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)/lectures/(?P<lecture_id>\d+)$', 'app.views.lecture', name='lecture'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)/tests/(?P<test_id>\d+)$', 'app.views.test', name='test'),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),
    url(r'^admin/', include(admin.site.urls)),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
