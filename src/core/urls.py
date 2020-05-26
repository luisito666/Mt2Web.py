# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# cargando modulos de django
# from django.conf.urls import include, url
from django.conf.urls import url, include
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
    url('', index, name="index"),
    url('donaciones/', donaciones, name="donaciones"),
    # url('checkout/', PaymentwallCallbackView.as_view(), name="checkout"),
    url('account/', include('apps.account.urls', namespace='account')),
    
    # superponer estadisticas en index
    url('admin/', staff_member_required(getRegistroOn.as_view()), name='admin'),
    url('admin/', admin.site.urls),
    url('password/(?P<url>\w{0,40})$/', process_password, name='recuperar_p'),
    url('activar/(?P<url>\w{0,40})$', process_reg, name='activar_cuenta'),
    url('reenviaremail/$', RequestToken.as_view(), name='email'),
    url('markdownx/', include('markdownx.urls')),
    url('', include('apps.paginas.urls', namespace='paginas')),
    url('api/v1/', include('apps.api.urls', namespace='api'))
]

"""if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""
