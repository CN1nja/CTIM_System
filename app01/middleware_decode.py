from django.utils.deprecation import MiddlewareMixin
import json


# 解析post请求的数据
class Md1(MiddlewareMixin):
    # 请求中间件
    def process_request(self, requset):
        if requset.method != 'GET' and requset.META.get('CONTENT_TYPE') == 'application/json':
            data = json.loads(requset.body, encoding='utf8')  # json反序列化
            requset.data = data

    # 响应中间件
    def process_response(self, requset, response):
        return response
