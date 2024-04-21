#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : N1key
# @Time     : 2023/2/27 11:20
# @File     : cms_finger.py
import re

from django.http import JsonResponse
from django.views import View
from app01.utils.subdomain_data_json import text_to_json
import os


class DicmanageView(View):
    def post(self, request):
        if request.method == 'POST':
            res = {
                'code': 425,
                'msg': '请在输入框输入对应的字典数据',
                'self': None
            }
            file1_path = "E:/djangoProject/网络威胁情报自主监测平台/CTIM_System/api/tools/dirmap/dirmap.py"
            dirmap_path = os.path.dirname(file1_path)

            file2_path = "E:/djangoProject/网络威胁情报自主监测平台/CTIM_System/api/tools/wydomain/wydomain.py"
            wydoamin_path = os.path.dirname(file2_path)

            dirmap_dict = dirmap_path + '/data/dict_mode_dict.txt'
            wydomain_dict = wydoamin_path + "/dnspod.csv"
            # print(dirmap_dict)
            # print(wydomain_dict)

            data = request.data
            print(data)

            # 子域名的字典
            if list(data.keys())[0] == "domain_content":
                if not re.match(r'^\S+(\n\S+)*$', data.get('domain_content')):
                    res['msg'] = "输入数据不能包含空格！"
                    return JsonResponse(res)

                else:
                    data['domain_content'] += '\n'
                    with open(wydomain_dict, 'a+') as f:
                        f.write(data['domain_content'])

                    res['code'] = 0
                    res['msg'] = '子域名扫描字典提交成功'

                    return JsonResponse(res)

            # 敏感路径的字典
            if list(data.keys())[0] == "path_content":
                if not re.match(r'^\S+(\n\S+)*$', data.get('path_content')):
                    res['msg'] = "输入数据不能包含空格！"
                    return JsonResponse(res)

                else:
                    data['path_content'] += '\n'
                    with open(dirmap_dict, 'a+') as f:
                        f.write(data['path_content'])

                    res['code'] = 0
                    res['msg'] = '敏感路径字典提交成功'

                    return JsonResponse(res)
