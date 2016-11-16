from django.conf.urls import url
from . import views

app_name = 'priceAnalysis'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<cabe_id>[0-9]+)$', views.detail, name='detail'),
    url(r'^datacabe/$', views.list, name='list'),
    url(r'^simple_chart/$',views.simple_chart,name="simple_chart"),
]
