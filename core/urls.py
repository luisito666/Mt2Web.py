# Copyright (c) 2017-2018 luispenagos91@gmail.com
# Distribuido bajo la licencia MIT Software Licence
# Mas informacion http://www.opensource.org/licenses/mit-license.php

from django.conf.urls import include, url
from django.contrib import admin
from .views import index, donaciones
from apps.account.views import process_password, process_reg, RequestToken
from django.contrib.admin.views.decorators import staff_member_required
from apps.administracion.estadisticas.views import getRegistroOn
from core import schedule2

# Url principales.
# Descomectar checkout si tiene implementado paymentwall
urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^donaciones$', donaciones, name="donaciones"),
    # url(r'^checkout/$', PaymentwallCallbackView.as_view(), name="checkout"),
    url(r'^account/', include('apps.account.urls', namespace='account')),
    #superponer estadisticas en index
    url(r'^admin/$', staff_member_required(getRegistroOn.as_view()), name='admin'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^password/(?P<url>\w{0,40})$', process_password, name='recuperar_p'),
    url(r'^activar/(?P<url>\w{0,40})$', process_reg, name='activar_cuenta'),
    url(r'^reenviaremail/$', RequestToken.as_view(), name='email'),
]

"""if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""


def ha():
    from apps.administracion.estadisticas.models import registroConectados
    from apps.player.models import Player
    from django.utils import timezone
    from datetime import timedelta
    from apps.varios.models import Top

    now = timezone.now()
    count = Player.objects.all().filter(last_play__range=[now - timedelta(minutes=55), now]).count()
    registroConectados(time=now, count=count).save()

    def getLastIdTop():
        try:
            last_id = Top.objects.values('id').last()['id']
            return last_id
        except:
            return 0

    b = Player.objects.values('id', 'name', 'job', 'level', 'exp').filter(id__gt=getLastIdTop())
    for i in b:
        Top.objects.create(**i)


schedule2.every(1).hours.at(0).do(ha)
schedule2.run_continuously()