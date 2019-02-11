# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# imporacion por defecto
from django.urls import path

from .views import SignUpApi, RankingPlayers, RankingGuilds

urlpatterns = [
    path('signup/', SignUpApi.as_view(), name='signup_api' ),
    path('players_ranking/', RankingPlayers.as_view(), name='players_ranking'),
    path('guilds_ranking/', RankingGuilds.as_view(), name='guilds_ranking')
]