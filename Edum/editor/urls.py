from django.conf.urls import patterns, url

urlpatterns = patterns('editor.views',
    url(r'^courses/merge_course/(?P<action>\w+)/(?P<course_id>[\d\w]+)$', 'merge_course', name='merge_course'),
    url(r'^courses/(?P<course_id>\d+)/merge_module/(?P<action>\w+)/(?P<module_id>[\d\w]+)$', 'merge_module', name='merge_module'),
    url(r'^courses/modules/(?P<module_id>\d+)/merge_lecture/(?P<action>\w+)/(?P<lecture_id>[\d\w]+)$', 'merge_lecture', name='merge_lecture'),
    url(r'^courses/modules/(?P<module_id>\d+)/merge_test/(?P<action>\w+)/(?P<test_id>[\d\w]+)$', 'merge_test', name='merge_test'),

    url(r'^courses/(?P<course_id>\d+)$', 'edit_course', name='edit_course'),
    url(r'^courses/(?P<course_id>\d+)/modules$', 'edit_modules', name='edit_modules'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)/lectures$', 'edit_lectures', name='edit_lectures'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)/tests$', 'edit_tests', name='edit_tests'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)/tests/(?P<test_id>\d+)$', 'edit_test', name='edit_test'),
)


