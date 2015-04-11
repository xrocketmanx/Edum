
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'app.views.home', name='home'),
    url(r'^contact$', 'app.views.contact', name='contact'),
    url(r'^about$', 'app.views.about', name='about'),
    url(r'^courses$', 'app.views.courses', name='courses'),
    url(r'^courses/(?P<course_id>\d+)$', 'app.views.course', name='course'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)$', 'app.views.module', name='module'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)/lectures/(?P<lecture_id>\d+)$', 'app.views.lecture', name='lecture'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)/tests/(?P<test_id>\d+)$', 'app.views.test', name='test'),
)



