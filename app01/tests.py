#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : N1key
# @Time     : 2023/3/4 22:20
# @File     : 1.py

import re

hash_str = 'a8398d30c7f641b4bb357e9bf3183ad2'
def is_valid_hash(hash_str):
    # 定义正则表达式，匹配32个字符（小写字母或数字）
    pattern = r'^[a-f0-9]{32}$'
    # 进行匹配
    match = re.match(pattern, hash_str)
    # 如果匹配成功，则返回 True，否则返回 False
    return match is not None

print(is_valid_hash(hash_str))