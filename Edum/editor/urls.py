from django.conf.urls import patterns, url
from editor.views import *

urlpatterns = patterns('editor.views',
    url(r'^courses/add$', 'create_course', name='add_course'),
    url(r'^courses/update/(?P<pk>\d+)$', 'update_course', name='update_course'),
    url(r'^courses/delete/(?P<pk>\d+)$', 'delete_course', name='delete_course'),
    url(r'^courses/(?P<course_id>\d+)/modules/add$', 'create_module', name='add_module'),
    url(r'^courses/(?P<course_id>\d+)/modules/update/(?P<pk>\d+)$', 'update_module', name='update_module'),
    url(r'^courses/(?P<course_id>\d+)/modules/delete/(?P<pk>\d+)$', 'delete_module', name='delete_module'),
    url(r'^courses/modules/(?P<module_id>\d+)/lectures/add$', 'create_lecture', name='add_lecture'),
    url(r'^courses/modules/(?P<module_id>\d+)/lectures/update/(?P<pk>\d+)$', 'update_lecture', name='update_lecture'),
    url(r'^courses/modules/(?P<module_id>\d+)/lectures/delete/(?P<pk>\d+)$', 'delete_lecture', name='delete_lecture'),
    url(r'^courses/modules/(?P<module_id>\d+)/tests/add$', 'create_test', name='add_test'),
    url(r'^courses/modules/(?P<module_id>\d+)/tests/update/(?P<pk>\d+)$', 'update_test', name='update_test'),
    url(r'^courses/modules/(?P<module_id>\d+)/tests/delete/(?P<pk>\d+)$', 'delete_test', name='delete_test'),
    url(r'^courses/modules/tests/(?P<test_id>\d+)/questions/add$', 'create_question', name='add_question'),
    url(r'^courses/modules/tests/(?P<test_id>\d+)/questions/update/(?P<pk>\d+)$', 'update_question', name='update_question'),
    url(r'^courses/modules/tests/(?P<test_id>\d+)/questions/delete/(?P<pk>\d+)$', 'delete_question', name='delete_question'),
    url(r'^courses/modules/tests/questions/(?P<question_id>\d+)/answers/add$', 'create_answer', name='add_answer'),
    url(r'^courses/modules/tests/questions/(?P<question_id>\d+)/answers/update/(?P<pk>\d+)$', 'update_answer', name='update_answer'),
    url(r'^courses/modules/tests/questions/(?P<question_id>\d+)/answers/delete/(?P<pk>\d+)$', 'delete_answer', name='delete_answer'),

    url(r'^courses/(?P<course_id>\d+)$', EditCourse.as_view(), name='edit_course'),
    url(r'^courses/(?P<course_id>\d+)/modules$', EditModules.as_view(), name='edit_modules'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)/lectures$', EditLectures.as_view(), name='edit_lectures'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)/tests$', EditTests.as_view(), name='edit_tests'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)/tests/(?P<test_id>\d+)$', EditTest.as_view(), name='edit_test'),
)


