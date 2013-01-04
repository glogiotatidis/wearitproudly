from django.conf import settings
from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'mozshirt.chest.views.home', name='home'),
    url(r'^shirt/(?P<shirt_id>\d+)/$', 'mozshirt.chest.views.view_shirt',
        name='view_shirt'),
    url(r'^shirt/(?P<shirt_id>\d+)/ownit/$', 'mozshirt.chest.views.own_shirt',
        name='own_shirt'),
    url(r'^shirt/(?P<shirt_id>\d+)/ownitnot/$', 'mozshirt.chest.views.own_shirt',
        {'add': False}, name='own_shirt_not'),
    url(r'^shirt/(?P<shirt_id>\d+)/add/$', 'mozshirt.chest.views.add_shot',
        name='add_shirt_shot'),
    url(r'^shirt/add/$', 'mozshirt.chest.views.add_shirt',
        name='add_shirt'),
    url(r'^shirt/(?P<shirt_id>\d+)/edit/$', 'mozshirt.chest.views.add_shirt',
        name='edit_shirt'),
    url(r'^tag/(?P<tag>.*)/$', 'mozshirt.chest.views.tag_gallery',
        name='tag_gallery'),
    url(r'^user/(?P<user_id>\d+)/$', 'mozshirt.chest.views.view_user',
        name='view_user'),
    url(r'^user/edit/$', 'mozshirt.chest.views.edit_user',
        name='edit_user'),
)
