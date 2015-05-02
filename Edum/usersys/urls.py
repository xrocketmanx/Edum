from django.conf.urls import patterns, url

urlpatterns = patterns('usersys.views',
    url(r'^login', 'login', name='login'),
    url(r'^logout', 'logout', name='logout'),
    url(r'^register', 'register', name='register'),
    url(r'^success', 'success', name='success'),
    url(r'^(?P<user_id>\d+)/token/(?P<token>\w+)', 'user_confirmation', name='user_confirmation'),
)
