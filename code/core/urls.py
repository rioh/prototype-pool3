from django.conf.urls import patterns, url
from . import views


urlpatterns = patterns(
    '',
    url(r'^$', views.homepage, name='homepage'),
    url(r'^about/$', views.about, name='about'),
    # url(r'^contact/$', views.contact, name='contact'),
    url(r'^accessibility/$', views.accessibility, name='accessibility'),
    url(r'^browse/events/$', views.browse, {'browse_type': "events"}, name='browse_events'),
    url(r'^browse/labels/$', views.browse, {'browse_type': "labels"}, name='browse_labels'),
    url(r'^browse/enforcements/$', views.browse, {'browse_type': "enforcements"},
        name='browse_enforcements'),
    url(r'^browse/manufacturers/$', views.browse, {'browse_type': 'manufacturers'},
        name='browse_manufacturers'),
    url(r'^search/labels/$', views.search_labels, name='search_labels'),
    url(r'^search/events/$', views.search_events, name='search_events'),
    url(r'^search/enforcements/$', views.search_enforcements, name='search_enforcements'),
    url(r'^search/manufacturers/$', views.search_manufacturers, name='search_manufacturers'),
    url(r'^search_detail/$', views.search_detail, name='search_detail'),
)
