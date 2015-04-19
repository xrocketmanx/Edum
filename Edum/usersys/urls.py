from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^login', 'usersys.views.login', name='login'),
    url(r'^logout', 'usersys.views.logout', name='logout'),
    url(r'^register', 'usersys.views.register', name='register'),
)
