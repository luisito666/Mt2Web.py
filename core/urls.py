# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# cargando modulos de django
# from django.conf.urls import include, url
from django.urls import path, include
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required

# cargando modulos locales
from apps.account.views import process_password, process_reg, RequestToken
from apps.administracion.estadisticas.views import getRegistroOn
from .views import index, donaciones

# cargando modulo de tareas en segundo plano.
from core import task

# Url principales.
# Descomectar checkout si tiene implementado paymentwall
urlpatterns = [
    path('', index, name="index"),
    path('donaciones/', donaciones, name="donaciones"),
    # path('checkout/', PaymentwallCallbackView.as_view(), name="checkout"),
    path('account/', include(('apps.account.urls', 'account'), namespace='account')),
    
    # superponer estadisticas en index
    path('admin/', staff_member_required(getRegistroOn.as_view()), name='admin'),
    path('admin/', admin.site.urls),
    path('password/<str:url>/', process_password, name='recuperar_p'),
    path('activar/<str:url>', process_reg, name='activar_cuenta'),
    path('reenviaremail/', RequestToken.as_view(), name='email'),
    path('markdownx/', include('markdownx.urls')),
    path('', include(('apps.paginas.urls', 'paginas'), namespace='pages')),
    path('api/v1/', include(('apps.api.urls', 'api'), namespace='api'))
]

"""if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""
