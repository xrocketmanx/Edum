from django.conf.urls import patterns, url

urlpatterns = patterns('app.views',
    url(r'^$', 'home', name='home'),
    url(r'^contact$', 'contact', name='contact'),
    url(r'^about$', 'about', name='about'),
    url(r'^courses$', 'courses', name='courses'),
    url(r'^courses/(?P<course_id>\d+)/like_course/(?P<view_name>\w+)$', 'like_course', name='like_course'),
    url(r'^courses/(?P<course_id>\d+)$', 'course', name='course'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)$', 'module', name='module'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)/lectures/(?P<lecture_id>\d+)$', 'lecture', name='lecture'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)/tests/(?P<test_id>\d+)$', 'test', name='test'),
)



