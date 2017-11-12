from django.conf.urls import url
from apps.account import views

urlpatterns = [
    #url(r'^show/(?P<pk>\d+)/$', views.ShowView.as_view(), name = 'show'),    
    url(r'^create/$', views.Create.as_view(), name = 'create'),
    url(r'^exito/$', views.exito , name = 'exito'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^password/$', views.changepasswd, name='password'),
    url(r'^descargas/$', views.descarga, name='descarga'),
    url(r'^top/$', views.top.as_view(), name='top'),
    url(r'^top_g/$', views.top_g.as_view(), name='top_g'),
    url(r'^request_password/$', views.recuperar_password , name='request'),
    url(r'^unlock/$', views.desbuguear , name='unlock'),

]