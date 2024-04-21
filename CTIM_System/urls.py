from django.contrib import admin
from django.urls import path, re_path, include
from app01 import views


urlpatterns = [
    path('webmaster/', admin.site.urls),
    path('', views.index),
    path('login/', views.login),
    path('sign/', views.sign),
    path('logout/', views.logout),
    path('login/random_code/', views.get_random_code),
    path('subdomain/', views.subdomain),  # 子域名检测
    path('pathscan/', views.pathscan),  # 敏感路径扫描
    path('dicmanage/', views.dicmanage),  # 字典管理
    path('cmsfinger/', views.cmsfinger),  # CMS指纹识别
    path('pushplus/', views.pushplus),  # 信息推送服务
    path('helpdoc/', views.helpdoc),  # 帮助文档

    path('attack/time/', views.attack_time),  # 攻击时间折线图
    path('attack_event/', views.attack_event),  # 攻击事件列表
    path('event_radar/', views.event_radar),  # 事件雷达

    re_path(r'^api/', include('api.urls')),  # 路由分发，将所有以 api 的请求分发到api/urls.py 中
]
