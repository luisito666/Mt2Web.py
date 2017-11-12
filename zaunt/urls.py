from django.conf.urls import include, url
from django.contrib import admin
from .views import index, donaciones
from apps.account.views import process_password, process_reg
#from django.conf import settings
#from django.conf.urls.static import static

urlpatterns = [
    # Examples:
    # url(r'^$', 'metin2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', index , name="index"),
    url(r'^donaciones$', donaciones, name="donaciones"),
    url(r'^account/', include('apps.account.urls', namespace='account')),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^markdown/', include("django_markdown.urls")),
    #url(r'^blog/', include("apps.blog.urls", namespace='blog')),
    url(r'^password/(?P<url>\w{0,40})$', process_password, name='recuperar_p' ),
    url(r'^activar/(?P<url>\w{0,40})$', process_reg, name='activar_cuenta' ),
    url(r'^api/', include('apps.rest.urls', namespace='rest')),
]

"""if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
"""