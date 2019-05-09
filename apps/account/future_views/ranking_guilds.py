# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# Django imports
from django.views.generic import ListView

# import models
from apps.player.models import Guild

# import funciones
from apps.account.funciones import guild_top, lenguaje

# Clase usada para renderizar el top del juego y paginarlo
class RankingGuilds(ListView):
    model = Guild
    template_name = 'account/ranking_guilds.html'
    queryset = guild_top()
    paginate_by = 20

    def get(self, request):
        lenguaje(request)
        return super(RankingGuilds, self).get(request)

