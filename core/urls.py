from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^$', 'core.views.index', name='digitalpuddle.index'),
)
