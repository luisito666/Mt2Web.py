# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# imporacion por defecto
from django.conf.urls import url

from .views import SignUpApi, RankingPlayers, RankingGuilds, TokenObtainView

urlpatterns = [
    url('signup/$', SignUpApi.as_view(), name='signup_api' ),
    url('players_ranking/$', RankingPlayers.as_view(), name='players_ranking'),
    url('guilds_ranking/$', RankingGuilds.as_view(), name='guilds_ranking'),
    url('token/$', TokenObtainView.as_view(), name='login')
]