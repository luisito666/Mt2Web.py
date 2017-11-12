from django.conf.urls import include, url
from apps.blog import views, feed

urlpatterns = [
    # Examples:
    # url(r'^$', 'metin2.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^feed/$', feed.UltimosPost(), name="feed"  ),
    url(r'^$', views.BlogIndex.as_view() , name="index"),
    url(r'(?P<slug>\S+)$', views.BlogDetail.as_view(), name="entry_detail" ),
]