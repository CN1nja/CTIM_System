#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : N1key
# @Time     : 2023/3/6 14:34
# @File     : cms_data_json.py

import json


def text_to_json(text_path):
    # 将字符串按行分割成列表
    with open(text_path, 'r') as f:
        data = f.readlines()

    del data[1]
    # 将剩下的行合并并转换为字典
    result = {}
    for line in data:
        key, value = line.strip().split(': ')
        result[key] = value
    # print(result)
    # 转换为 JSON 格式并打印
    cms_data = json.dumps(result)
    return cms_data


if __name__ == '__main__':
    text_to_json()
