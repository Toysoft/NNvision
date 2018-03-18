from django.conf import settings
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^camera/$', views.camera, name='camera'),
    url(r'^darknet/$', views.darknet, name='darknet'),
    url(r'^darknet/state/$', views.darknet_state, name='ds'),
    path('panel/<int:first>', views.panel, name='panel'),
    path('alert', views.alert, name='alertl'),
    #url(r'^panel/(?P<first>\d+)$', views.panel, name='panel'),
    url(r'^panel/detail/(?P<id>\d+)$', views.panel_detail, name='detail'),
    url(r'^settings/$', views.configuration, name='configuration'),
    url(r'^settings/wifi_add/$', views.wifi_add, name='wifi_add'),
    url(r'^settings/wifi_suppr/$', views.wifi_suppr, name='wifi_suppr'),
    url(r'^settings/wifi_restart/$', views.wifi_restart, name='wifi_restart'),
    url(r'^reboot/', views.reboot, name='reboot'),
    url(r'^shutdown/', views.shutdown, name='shutdown'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)