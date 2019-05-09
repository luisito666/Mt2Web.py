# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

# imporacion por defecto
from django.urls import path

# Importando vistas para el correcto funcionamiento de las urls
from apps.paginas import views

# urls del proyecto
urlpatterns = [
    path('<slug:slug>', views.PageDetail.as_view(), name='page_details'),
]
