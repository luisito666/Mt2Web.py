# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# Django imports
from django.views.generic import ListView

# import models
from apps.varios.models import Top

# import funciones
from apps.account.funciones import player_top, lenguaje

# clase usada para la pagina del ranking del juego y paginarlo
class RankingPlayers(ListView):
    model = Top
    template_name = 'account/ranking_players.html'
    queryset = player_top()
    paginate_by = 20

    def get(self, request):
        lenguaje(request)
        return super(RankingPlayers, self).get(request)

