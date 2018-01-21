# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

#imporacion por defecto
from django.conf.urls import url

#Importando vistas para el correcto funcionamiento de las urls
from apps.account import views

#urls del proyecto
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
