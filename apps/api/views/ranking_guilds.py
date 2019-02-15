# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# Rest Framework
from rest_framework import generics

# Models
from apps.player.models import Guild

# Serializers
from apps.api.serializers import RankingGuildSerializer

from apps.api.authentication import TokenAuthentication

# Pagination
from apps.api.pagination import RankinPageNumber
from apps.api.permissions import IsAuthenticated

class RankingGuilds(generics.ListAPIView):
	queryset = Guild.objects.all().order_by('-level','-exp','-win', '-ladder_point')
	serializer_class = RankingGuildSerializer
	pagination_class = RankinPageNumber
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)

