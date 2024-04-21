#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : N1key
# @Time     : 2023/3/6 20:16
# @File     : domaindata_down.py
from django.http import HttpResponse


def Domaindata_down(request):
    data_path = "E:/djangoProject/网络威胁情报自主监测平台/CTIM_System/api/tools/Data_storage/domain_data.xlsx"
    # 打开导出的Excel文件
    with open(data_path, 'rb') as f:
        # 创建一个HttpResponse对象来返回Excel文件
        response = HttpResponse(f.read(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=domain_data.xlsx'
        return response
