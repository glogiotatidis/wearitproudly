from django.conf.urls import patterns, url

urlpatterns = patterns('mozshirt.auth.views',
    url(r'verify/$', 'mozilla_browserid_verify', name='my_browserid_verify'),
    url(r'failed/$', 'login_failure', name='login_failure'),
    url(r'logout/$', 'logout', name='logout'),
)
