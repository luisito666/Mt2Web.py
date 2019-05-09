# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

from django.utils.deprecation import MiddlewareMixin
from apps import authentication as auth
from django.utils.functional import SimpleLazyObject


def get_user(request):
    if not hasattr(request, '_cached_account'):
        request._cache_account = auth.get_user(request)
    return request._cache_account


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # assert hasattr(request, 'session')
        request.account = SimpleLazyObject(lambda: get_user(request))

