from django.conf.urls import patterns, url, include
import socketio.sdjango

socketio.sdjango.autodiscover()

urlpatterns = patterns('',
    url("^socket\.io", include(socketio.sdjango.urls)),
    url(r'^$', 'core.views.index', name='digitalpuddle.index'),
    url(r'^create/$', 'core.views.create_virtual_machine', name='digitalpuddle.create_virtual_machine')
)
