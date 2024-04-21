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
from app01.utils.subdomain_data_json import text_to_json


class SubdomainView(View):
    def post(self, request):
        if request.method == 'POST':
            res = {
                'data': None,
                'self': None,
                'msg': "请输入域名！",
                'code': 425,
            }
            data = request.data  # 请求体
            domain_name = data.get('domain')
            print(domain_name)
            if not domain_name:
                return JsonResponse(res)

            # 匹配域名的正则表达式
            pattern = r'^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,6}$'
            if not re.match(pattern, domain_name):
                res['msg'] = "域名格式输入错误！"
                return JsonResponse(res)

            file_path = "E:/djangoProject/网络威胁情报自主监测平台/CTIM_System/api/tools/wydomain/wydomain.py"
            dir_path = os.path.dirname(file_path)
            # print(dir_path)
            # 执行扫描子域名的脚本
            cmd_str = 'cd ' + dir_path + ' & ' + "python dnsburte.py -d " + domain_name + " -f " + "dnspod.csv -o " + domain_name + '.log'
            f = os.system(cmd_str)
            print(f)

            # 读取cmd解析出的网站敏感路径文本
            path_text = dir_path + '/' + domain_name + '.log'
            json_data = text_to_json(path_text)
            # print(json_data)

            res['data'] = json_data
            res['self'] = 1
            res['code'] = 0
            res['msg'] = "数据加载成功！"

            # 将数据转换为DataFrame对象
            path_data = json.loads(json_data)
            df = pd.DataFrame(path_data)
            # 将数据保存为Excel文件
            data_path = "E:/djangoProject/网络威胁情报自主监测平台/CTIM_System/api/tools/Data_storage/domain_data.xlsx"
            df.to_excel(data_path, index=False)

            # 推送服务
            pushplus(json_data, "子域名检测", domain_name)
            return JsonResponse(res, safe=False)
