# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# Rest framewrok
from rest_framework.views import APIView
from rest_framework.response import Response

# local serializers
from apps.api.serializers import RegisterSerializer, SigupSerializer

class SignUpApi(APIView):

	def post(self, request, format=None):
		serializer = SigupSerializer(data = request.data)
		if serializer.is_valid(raise_exception=True):
			return Response(serializer.validated_data)
		return Response(serializer.errors)
