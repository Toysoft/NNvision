from django import VERSION as v
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from . import views

if v[0] >=2 : 
    from django.urls import path, include
    urlpatterns = [
        path('accounts/', include('django.contrib.auth.urls')),
        url(r'^$', views.index, name='index'),
        url(r'^camera/$', views.camera, name='camera'),
        url(r'^darknet/$', views.darknet, name='darknet'),
        url(r'^darknet/state/$', views.darknet_state, name='ds'),
        path('panel/<int:first>/<int:first_alert>', views.panel, name='panel'),
        path('warning/<int:first_alert>', views.warning, name='warning'),
        path('alert/', views.alert, name='alert'),
        path('alert/suppr/<int:id>', views.alert, name='alert'),
        path('alert/suppr_auto/<int:id2>', views.alert, name='alert'),
        url(r'^panel/detail/(?P<id>\d+)$', views.panel_detail, name='detail'),
        url(r'^settings/$', views.configuration, name='configuration'),
        url(r'^settings/wifi_add/$', views.wifi_add, name='wifi_add'),
        url(r'^settings/wifi_suppr/$', views.wifi_suppr, name='wifi_suppr'),
        url(r'^settings/wifi_restart/$', views.wifi_restart, name='wifi_restart'),
        path('camera/last/<int:cam>', views.last, name='last image'),
        path('img/last/<int:cam_id>', views.get_last_analyse_img, name='image'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
else :
    from django.conf.urls import include
    urlpatterns = [
        url(r'^accounts/', include('django.contrib.auth.urls')),
        url(r'^$', views.index, name='index'),
        url(r'^camera/$', views.camera, name='camera'),
        url(r'^camera/last/(?P<cam>\d+)$', views.last, name='last image'),
        url(r'^darknet/$', views.darknet, name='darknet'),
        url(r'^darknet/state/$', views.darknet_state, name='ds'),
        url(r'^panel/(?P<first>\d+)/(?P<first_alert>\d+)$', views.panel, name='panel'),
        url(r'^warning/(?P<first_alert>\d+)$', views.warning, name='warning'),
        url(r'^alert/$', views.alert, name='alert'),
        url(r'^alert/suppr/(?P<id>\d+)$', views.alert, name='alert'),
        url(r'^alert/suppr_auto/(?P<id2>\d+)$', views.alert, name='alert'),
        url(r'^panel/detail/(?P<id>\d+)$', views.panel_detail, name='detail'),
        url(r'^settings/$', views.configuration, name='configuration'),
        url(r'^settings/wifi_add/$', views.wifi_add, name='wifi_add'),
        url(r'^settings/wifi_suppr/$', views.wifi_suppr, name='wifi_suppr'),
        url(r'^settings/wifi_restart/$', views.wifi_restart, name='wifi_restart'),
        url(r'^camera/last/(?P<cam_id>\d+)$', views.get_last_analyse_img, name='image'),
        url('img/last/(?P<cam_id>\d+)$', views.get_last_analyse_img, name='image'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    
