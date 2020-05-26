# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# imporacion por defecto
from django.conf.urls import url

from .views import SignUpApi, RankingPlayers, RankingGuilds, TokenObtainView

urlpatterns = [
    url(r'signup/$', SignUpApi.as_view(), name='signup_api' ),
    url(r'players_ranking/$', RankingPlayers.as_view(), name='players_ranking'),
    url(r'guilds_ranking/$', RankingGuilds.as_view(), name='guilds_ranking'),
    url(r'token/$', TokenObtainView.as_view(), name='login')
]