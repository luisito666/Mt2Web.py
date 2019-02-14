# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

from django.utils.deprecation import MiddlewareMixin
from apps.authentication import get_user
from django.utils.functional import SimpleLazyObject


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # assert hasattr(request, 'session')
        request.account = SimpleLazyObject(lambda: get_user(request))