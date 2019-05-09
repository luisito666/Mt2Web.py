# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

from django.utils.deprecation import MiddlewareMixin
from .models import Account


def get_user(request):
    if not hasattr(request, '_cached_account'):
        try:
            cuenta = Account.objects.get(id=request.session['g1jwvO'])
            request._cached_account = cuenta
        except Exception as e:
            request._cached_account = 'nologin'
    return request._cached_account


class AccountMiddleware(MiddlewareMixin):
    def process_request(self, request):
        assert hasattr(request, 'session')
        request.account = get_user(request)
