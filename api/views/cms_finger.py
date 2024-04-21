#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : N1key
# @Time     : 2023/2/27 11:20
# @File     : cms_finger.py
import json
import re

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from api.views.pushplus import pushplus
from app01.utils.cms_data_json import text_to_json
import os
import subprocess


class CmsfingerView(View):
    def post(self, request):
        if request.method == 'POST':
            res = {
                'msg': "请输入网址！",
                'code': 425,
            }
            data = request.data
            cms_site = data.get('cms_site')
            print(cms_site)
            if not cms_site:
                return JsonResponse(res)

            if not re.match(r'^https?:/{2}\w.+$', cms_site):
                res['msg'] = "URL地址格式输入错误！"
                return JsonResponse(res)

            file_path = "E:/djangoProject/网络威胁情报自主监测平台/CTIM_System/api/tools/TideFinger_CMS/python3/TideFinger.py"
            dir_path = os.path.dirname(file_path)
            output = dir_path + '/output.txt'
            # print(dir_path)

            result = subprocess.run(['python3', dir_path + '/TideFinger.py', '-u', cms_site], capture_output=True,
                                    text=True)
            with open(output, 'w', encoding='utf-8') as f:
                f.write(result.stdout)

            res['code'] = 0
            res['msg'] = "数据输出成功！"

            # 读取cmd解析出的网站敏感路径文本
            json_data = text_to_json(output)
            print(json_data)

            pushplus(json_data, "CMS指纹识别", cms_site)
            return JsonResponse(res)
