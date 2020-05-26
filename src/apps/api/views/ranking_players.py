# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# Rest Framework
from rest_framework import generics

# Models
from django.db.models import Q
from apps.varios.models import Top

# Serializers
from apps.api.serializers import RankingPlayerSerializer

# Pagination
from apps.api.pagination import RankinPageNumber


class RankingPlayers(generics.ListAPIView):
	queryset = Top.objects.all().exclude(Q(name__contains='[')).order_by('-level','-exp')
	serializer_class = RankingPlayerSerializer
	pagination_class = RankinPageNumber

