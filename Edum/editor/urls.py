from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^courses/merge_course/(?P<action>\w+)/(?P<course_id>[\d\w]+)$', 'editor.views.merge_course', name='merge_course'),
    url(r'^courses/(?P<course_id>\d+)/merge_module/(?P<action>\w+)/(?P<module_id>[\d\w]+)$', 'editor.views.merge_module', name='merge_module'),
    url(r'^courses/modules/(?P<module_id>\d+)/merge_module/(?P<action>\w+)/(?P<lecture_id>[\d\w]+)$', 'editor.views.merge_lecture', name='merge_lecture'),
    url(r'^courses/(?P<course_id>\d+)$', 'editor.views.edit_course', name='edit_course'),
    url(r'^courses/(?P<course_id>\d+)/modules$', 'editor.views.edit_modules', name='edit_modules'),
    url(r'^courses/(?P<course_id>\d+)/modules/(?P<module_id>\d+)/lectures$', 'editor.views.edit_lectures', name='edit_lectures'),
)


