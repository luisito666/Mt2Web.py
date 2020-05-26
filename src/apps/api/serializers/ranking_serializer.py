# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

from rest_framework import serializers


class RankingPlayerSerializer(serializers.Serializer):
	account_id = serializers.IntegerField()
	name = serializers.CharField()
	guild_name = serializers.CharField()
	level = serializers.IntegerField()
	exp = serializers.IntegerField()
	ranking = serializers.IntegerField()


class RankingGuildSerializer(serializers.Serializer):
    name = serializers.CharField()
    level = serializers.IntegerField()
    exp = serializers.IntegerField()
    ladder_point = serializers.IntegerField()

