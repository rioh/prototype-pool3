from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.homepage, name='homepage'),
    url(r'^browse/events/$', views.browse, {'browse_type': "events"}, name='browse_events'),
    url(r'^browse/labels/$', views.browse, {'browse_type': "labels"}, name='browse_labels'),
    url(r'^browse/enforcements/$', views.browse, {'browse_type': "enforcements"}, name='browse_enforcements'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search_detail/$', views.search_detail, name='search_detail'),
)
