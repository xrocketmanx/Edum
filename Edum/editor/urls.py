from django.conf.urls import patterns, url
from editor.views import *

urlpatterns = patterns('editor.views',
    url(r'^courses/add$', CourseCreator.as_view(), name='add_course'),
    url(r'^courses/update/(?P<pk>\d+)$', CourseUpdater.as_view(), name='update_course'),
    url(r'^courses/delete/(?P<pk>\d+)$', CourseDeleter.as_view(), name='delete_course'),
    url(r'^courses/(?P<course_id>\d+)/merge_module/(?P<action>\w+)/(?P<module_id>[\d\w]+)$', 'merge_module', name='merge_module'),
    url(r'^courses/modules/(?P<module_id>\d+)/merge_lecture/(?P<action>\w+)/(?P<lecture_id>[\d\w]+)$', 'merge_lecture', name='merge_lecture'),
    url(r'^courses/modules/(?P<module_id>\d+)/merge_test/(?P<action>\w+)/(?P<test_id>[\d\w]+)$', 'merge_test', name='merge_test'),

    url(r'^courses/(?P<course_id>\d+)$', EditCourse.as_view(), name='edit_course'),
    url(r'^courses/(?P<course_id>\d+)/modules$', EditModules.as_view(), name='edit_modules'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)/lectures$', EditLectures.as_view(), name='edit_lectures'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)/tests$', EditTests.as_view(), name='edit_tests'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)/tests/(?P<test_id>\d+)$', EditTest.as_view(), name='edit_test'),
)


