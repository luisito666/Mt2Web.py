# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

from django.conf.urls import include, url
from django.contrib import admin
from .views import index, donaciones
from apps.account.payview import PaymentwallCallbackView
from apps.account.views import process_password, process_reg
#from django.conf import settings
#from django.conf.urls.static import static

#Url principales.
#Descomectar checkout si tiene implementado paymentwall
urlpatterns = [
    url(r'^$', index , name="index"),
    url(r'^donaciones$', donaciones, name="donaciones"),
    #url(r'^checkout/$', PaymentwallCallbackView.as_view(), name="checkout"),
    url(r'^account/', include('apps.account.urls', namespace='account')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^password/(?P<url>\w{0,40})$', process_password, name='recuperar_p' ),
    url(r'^activar/(?P<url>\w{0,40})$', process_reg, name='activar_cuenta' ),
]

"""if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""
