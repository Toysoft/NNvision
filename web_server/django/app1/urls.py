from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.urls import path, include
from . import views

favicon_view = RedirectView.as_view(url='/static/app1/img/favicon.ico', permanent=True)

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^camera/$', views.camera, name='camera'),
    path('panel/<str:nav>/<int:first>', views.panel, name='panel'),
    path('warning/<int:first_alert>', views.warning, name='warning'),
    path('warning_detail/<int:id>', views.warning_detail, name='warning_detail'),
    path('alert/', views.alert, name='alert'),
    path('alert/suppr/<int:id>', views.alert, name='alert'),
    path('alert/suppr_auto/<int:id2>', views.alert, name='alert'),
    path('panel_detail/<int:id>', views.panel_detail, name='detail'),
    path('camera/last/<int:cam>', views.last, name='last image'),
    path('img/last/<int:cam_id>', views.get_last_analyse_img, name='image'),
    path('thumbnail/<path:path_im>', views.thumbnail, name='thumbnail'),
    path('upload', views.upload),
    path('getCam', views.getCam),
    path('getScheme', views.getScheme),
    path('setCam', views.setCam),
    path('getState', views.getState),
    path('upCam', views.upCam),
    path('favicon.ico', favicon_view),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
