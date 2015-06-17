from django.conf.urls import patterns, url
from usersys.views import ProfileUpdater

urlpatterns = patterns('usersys.views',
    url(r'^profile$', 'profile', name='profile'),
    url(r'^update_profile/(?P<pk>\d+)$', ProfileUpdater.as_view(), name='update_profile'),
    url(r'^update_password$', 'update_password', name='update_password'),
    url(r'^login$', 'login', name='login'),
    url(r'^logout$', 'logout', name='logout'),
    url(r'^register$', 'register', name='register'),
    url(r'^success$', 'success', name='success'),
    url(r'^petition$', 'petition', name='petition'),
    url(r'^petition/accept/(?P<username>\w+)$', 'accept_petition', name='accept_petition'),
    url(r'^(?P<user_id>\d+)/token/(?P<token>\w+)$', 'user_confirmation', name='user_confirmation'),
)
