# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# imporacion por defecto
from django.conf.urls import url

# Importando vistas para el correcto funcionamiento de las urls
from apps.account import views

# urls del proyecto
urlpatterns = [
    # url(r'^show/(?P<pk>\d+)/$', views.ShowView.as_view(), name = 'show'),
    url('create/$', views.SignUp.as_view(), name='create'),
    url('exito/$', views.exito, name='exito'),
    url('login/$', views.Login.as_view(), name='login'),
    url('logout/$', views.logout, name='logout'),
    url('password/$', views.ResetPassword.as_view(), name='password'),
    url('descargas/$', views.Downloads.as_view(), name='descarga'),
    url('top/$', views.RankingPlayers.as_view(), name='top'),
    url('top_g/$', views.RankingGuilds.as_view(), name='top_g'),
    url('request_password/$', views.recuperar_password, name='request'),
    url('unlock/$', views.UnlockPlayer.as_view() , name='unlock'),
    url('request_username/$', views.RequestUsername.as_view(), name='request_username'),
]
