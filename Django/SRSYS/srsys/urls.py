from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'), # name用于反向解析
    url(r'^code/$', views.code,name='code'), # 验证码
    url(r'^result/$',views.result,name='result') # 成绩展示页面
    # url(r'^create_code/$',views.create_code_img), # 自己写的验证码程序
]
