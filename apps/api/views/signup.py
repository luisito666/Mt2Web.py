# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# Rest framewrok
from rest_framework.views import APIView
from rest_framework.response import Response

# local serializers
from apps.api.serializers import RegisterSerializer

class SignUpApi(APIView):

	def post(self, request, format=None):
		serializer = RegisterSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors)
