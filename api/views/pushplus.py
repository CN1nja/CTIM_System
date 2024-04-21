#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : N1key
# @Time     : 2023/3/6 12:19
# @File     : pushplus.py
import json
import re

import requests
from django.http import JsonResponse
from django.views import View


class PushplusView(View):
    def post(self, request):
        if request.method == 'POST':
            res = {
                'msg': "请输入token值！",
                'code': 425,
            }
            data = request.data  # 请求体
            token = data.get('token_info')
            print(token)

            if not token:
                return JsonResponse(res)

            # 定义正则表达式，匹配32个字符（小写字母或数字）
            pattern = r'^[a-f0-9]{32}$'
            # 进行匹配
            if not re.match(pattern, token):
                res['msg'] = "token格式有误，检测token是否输入正确！"
                return JsonResponse(res)

            token_store = "E:/djangoProject/网络威胁情报自主监测平台/CTIM_System/api/tools/Data_storage/token.txt"
            with open(token_store, "w") as f:
                f.write(token)
                res["msg"] = "修改token成功!"
                res['code'] = 0
                return JsonResponse(res)


def pushplus(json_data, module_name, site_name):
    token_store = "E:/djangoProject/网络威胁情报自主监测平台/CTIM_System/api/tools/Data_storage/token.txt"
    with open(token_store, 'r') as f:
        token_value = f.read()

    new_list = []
    json_data_list = json.loads(json_data)

    if module_name == "敏感路径扫描":
        for item in json_data_list:
            for key, value in item.items():
                all_value = '<br>' + key + " : " + value
                new_list.append(all_value)
            new_list.append('<br>')

    if module_name == "子域名检测":
        for item in json_data_list:
            for key, value in item.items():
                all_value = '<br>' + value
                new_list.append(all_value)

    if module_name == "CMS指纹识别":
        mapping = {"URL_address": "URL地址", "Banner": "Banner指纹信息", "CMS_finger": "CMS指纹信息"}
        new_data = {}
        for old_key, value in json_data_list.items():
            new_key = mapping.get(old_key, old_key)
            new_data[new_key] = value
        # print(new_data)
        for key in new_data:
            all_value = '<br>' + key + " : " + new_data[key]
            new_list.append(all_value + '<br>')


    # print(new_list)
    dic = {'测试站点为': site_name, '扫描已结束返回数据为': new_list}
    url = 'http://www.pushplus.plus/send'
    data = {
        "token": token_value,
        "title": module_name + '模块检测结果',
        "content": json.dumps(dic),
        "template": "json"
    }
    body = json.dumps(data).encode(encoding='utf-8')
    headers = {'Content-Type': 'application/json'}
    requests.post(url, data=body, headers=headers)
