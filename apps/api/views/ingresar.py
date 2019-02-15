
from apps.authentication.models import Account
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions

class AccountApiView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        try:
            user = Account.objects.get(login=username)
        except Account.DoesNotExist:
            raise exceptions.NotAuthenticated('username or password incorrect')
        token = user.generate_auth_token()
        #print(token)

        return Response({'token': token.decode('utf-8')})

