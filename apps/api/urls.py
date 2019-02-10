# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# imporacion por defecto
from django.urls import path

from .views import SignUpApi

urlpatterns = [
    path('signup/', SignUpApi.as_view(), name='signup_api' )
]