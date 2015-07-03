from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^', include('core.urls')),
)

handler400 = 'core.views.error400'
handler404 = 'core.views.error404'
handler500 = 'core.views.error500'