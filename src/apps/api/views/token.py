from __future__ import unicode_literals

from rest_framework import generics, status
from rest_framework.response import Response

from .. import serializers
from .. import authentication
from .. import exceptions 


class TokenViewBase(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = None

    www_authenticate_realm = 'api'

    def get_authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            authentication.AUTH_HEADER_TYPES,
            self.www_authenticate_realm,
        )
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except exceptions.TokenError as e:
            raise exceptions.InvalidToken(e.args[0])
        
        return Response(serializer.validated_data, status=status.HTTP_200_OK)



class TokenObtainView(TokenViewBase):
    """
    """
    serializer_class = serializers.TokenObtainSerializer



# token_obtain_pair = TokenObtainView.as_view()