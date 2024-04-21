#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : N1key
# @Time     : 2023/2/27 11:20
# @File     : cms_finger.py
import json
import re
import os
import pandas as pd
from django.http import JsonResponse
from django.views import View
from api.views.pushplus import pushplus
from app01.utils.pathscan_data_json import text_to_json


class PathscanView(View):
    def post(self, request):
        if request.method == 'POST':
            res = {
                'data': None,
                'self': None,
                'msg': "请输入网址！",
                'code': 425,
            }
            data = request.data  # 请求体
            url_link = data.get('link')
            print(url_link)
            if not url_link:
                return JsonResponse(res)

            if not re.match(r'^https?:/{2}\w.+$', url_link):
                res['msg'] = "URL地址格式输入错误！"
                return JsonResponse(res)

            file_path = "E:/djangoProject/网络威胁情报自主监测平台/CTIM_System/api/tools/dirmap/dirmap.py"
            dir_path = os.path.dirname(file_path)
            # print(dir_path)
            # 执行 dirmap脚本
            cmd_str = 'cd ' + dir_path + ' & ' + "python dirmap.py -i " + url_link + " -lcf"
            f = os.system(cmd_str)
            print(f)

            # 读取cmd解析出的网站敏感路径文本
            domain = url_link.split('/')[2]
            path_text = dir_path + '/output/' + domain + '.txt'
            json_data = text_to_json(path_text)

            res['data'] = json_data
            res['self'] = 1
            res['code'] = 0
            res['msg'] = '数据加载成功！'

            print(json_data)
            print(type(json_data))
            # 将数据转换为DataFrame对象
            path_data = json.loads(json_data)
            df = pd.DataFrame(path_data)
            # 将数据保存为Excel文件
            data_path = "E:/djangoProject/网络威胁情报自主监测平台/CTIM_System/api/tools/Data_storage/path_data.xlsx"
            df.to_excel(data_path, index=False)

            # 推送服务
            pushplus(json_data, "敏感路径扫描", url_link)
            return JsonResponse(res, safe=False)
