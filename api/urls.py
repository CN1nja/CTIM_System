from django.urls import path, re_path
from api.views import login, pathscan, subdomain, dicmanage, cms_finger, pushplus, pathdata_down, domaindata_down, \
    logdata_down

urlpatterns = [
    path('login/', login.LoginView.as_view()),  # 登录
    path('sign/', login.SignView.as_view()),  # 注册
    path('pathscan/', pathscan.PathscanView.as_view()),  # 敏感路径扫描
    path('subdomain/', subdomain.SubdomainView.as_view()),  # 子域名检测
    path('dicmanage/', dicmanage.DicmanageView.as_view()),  # 字典管理
    path('cmsfinger/', cms_finger.CmsfingerView.as_view()),  # CMS指纹识别
    path('pushplus/', pushplus.PushplusView.as_view()),  # 信息推送服务

    path('pathdata_down/', pathdata_down.Pathdata_down),  # 敏感路径数据下载
    path('domaindata_down/', domaindata_down.Domaindata_down),  # 子域名数据下载
    path('logdata_down/', logdata_down.Logdata_down),  # 攻击日志数据下载
]