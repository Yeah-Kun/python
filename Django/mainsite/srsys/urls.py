from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), # name用于反向解析
    url(r'^result/$',views.result,name='result')
]
