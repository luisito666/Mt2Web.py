from django.conf.urls import url
from apps.rest import views

urlpatterns = [
    #url(r'^show/(?P<pk>\d+)/$', views.ShowView.as_view(), name = 'show'),
    url(r'^users/(?P<login>\w{0,40})$', views.UsersDetail, name = 'users'),
    url(r'^stats/$', views.StatsDetail, name = 'stats'),
    url(r'^top5/$', views.Ranking, name = 'top5'),
    url(r'^top_g5/$', views.RankingGremios, name = 'top_g5'),
    url(r'^descargas/$', views.Descargas, name = 'descarga'),
    url(r'^top/$', views.TopList.as_view(), name = 'top5'),
    url(r'^top_g/$', views.GuidList.as_view(), name = 'top_g'),
    url(r'^registro/$', views.RegisterApi.as_view(), name = 'registro'),
]
