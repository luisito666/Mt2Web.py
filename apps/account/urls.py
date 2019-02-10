# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# imporacion por defecto
from django.urls import path

# Importando vistas para el correcto funcionamiento de las urls
from apps.account import views

# urls del proyecto
urlpatterns = [
    # url(r'^show/(?P<pk>\d+)/$', views.ShowView.as_view(), name = 'show'),
    path('create/', views.SignUp.as_view(), name='create'),
    path('exito/', views.exito, name='exito'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('password/', views.ResetPassword.as_view(), name='password'),
    path('descargas/', views.Downloads.as_view(), name='descarga'),
    path('top/', views.RankingPlayers.as_view(), name='top'),
    path('top_g/', views.RankingGuilds.as_view(), name='top_g'),
    path('request_password/', views.recuperar_password, name='request'),
    path('unlock/', views.desbuguear , name='unlock'),
    path('request_username/', views.RequestUsername.as_view(), name='request_username'),
]
