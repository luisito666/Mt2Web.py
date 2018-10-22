# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# imporacion por defecto
from django.conf.urls import url

# Importando vistas para el correcto funcionamiento de las urls
from apps.paginas import views

# urls del proyecto
urlpatterns = [
    url(r'(?P<slug>\S+)$', views.PageDetail.as_view(), name='page_details'),
]
