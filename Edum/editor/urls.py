from django.conf.urls import patterns, url
from editor.views import *

urlpatterns = patterns('editor.views',
    url(r'^courses/add$', CourseCreator.as_view(), name='add_course'),
    url(r'^courses/update/(?P<pk>\d+)$', CourseUpdater.as_view(), name='update_course'),
    url(r'^courses/delete/(?P<pk>\d+)$', CourseDeleter.as_view(), name='delete_course'),
    url(r'^courses/(?P<course_id>\d+)/modules/add$', ModuleCreator.as_view(), name='add_module'),
    url(r'^courses/(?P<course_id>\d+)/modules/update/(?P<pk>\d+)$', ModuleUpdater.as_view(), name='update_module'),
    url(r'^courses/(?P<course_id>\d+)/modules/delete/(?P<pk>\d+)$', ModuleDeleter.as_view(), name='delete_module'),
    url(r'^courses/modules/(?P<module_id>\d+)/lectures/add$', LectureCreator.as_view(), name='add_lecture'),
    url(r'^courses/modules/(?P<module_id>\d+)/lectures/update/(?P<pk>\d+)$', LectureUpdater.as_view(), name='update_lecture'),
    url(r'^courses/modules/(?P<module_id>\d+)/lectures/delete/(?P<pk>\d+)$', LectureDeleter.as_view(), name='delete_lecture'),
    url(r'^courses/modules/(?P<module_id>\d+)/tests/add$', TestCreator.as_view(), name='add_test'),
    url(r'^courses/modules/(?P<module_id>\d+)/tests/update/(?P<pk>\d+)$', TestUpdater.as_view(), name='update_test'),
    url(r'^courses/modules/(?P<module_id>\d+)/tests/delete/(?P<pk>\d+)$', TestDeleter.as_view(), name='delete_test'),

    url(r'^courses/(?P<course_id>\d+)$', EditCourse.as_view(), name='edit_course'),
    url(r'^courses/(?P<course_id>\d+)/modules$', EditModules.as_view(), name='edit_modules'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)/lectures$', EditLectures.as_view(), name='edit_lectures'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)/tests$', EditTests.as_view(), name='edit_tests'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)/tests/(?P<test_id>\d+)$', EditTest.as_view(), name='edit_test'),
)


