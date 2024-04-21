import os
import json
import pandas as pd
from django.contrib import auth
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from app01.utils.random_code import random_code
from datetime import datetime

# 获取随机验证码
def get_random_code(request):
    data, valid_code = random_code()
    request.session['valid_code'] = valid_code  # 将生成的验证码存储到 session中
    return HttpResponse(data)


# Create your views here.
def index(request):
    if not request.user.username:
        # 没有登录
        return redirect("/login/")
    return render(request, 'index.html', locals())


def login(request):
    return render(request, 'login.html')


def sign(request):
    return render(request, "sign.html")


def logout(request):
    auth.logout(request)
    return redirect('/')


def subdomain(request):
    if not request.user.username:
        # 没有登录
        return redirect("/login/")
    return render(request, "subdomain.html")


def pathscan(request):
    if not request.user.username:
        return redirect("/login/")
    return render(request, "pathscan.html")


def dicmanage(request):
    if not request.user.username:
        # 没有登录
        return redirect("/login/")
    return render(request, "dicmanage.html")


def cmsfinger(request):
    if not request.user.username:
        # 没有登录
        return redirect("/login/")

    file_path = "E:/djangoProject/网络威胁情报自主监测平台/CTIM_System/api/tools/TideFinger_CMS/python3/TideFinger.py"
    dir_path = os.path.dirname(file_path)
    output = dir_path + '/output.txt'
    with open(output, 'r', encoding='utf-8') as f:
        data = f.readlines()

    if not data:
        return render(request, "cms_finger.html", locals())

    # 删除第二行
    try:
        del data[1]
        # 将剩下的行合并并转换为字典
        result = {}
        for line in data:
            key, value = line.strip().split(': ')
            result[key] = value
        # print(result)
        # 转换为 JSON 格式并打印
        cms_data = json.dumps(result)
        cms_data = json.loads(cms_data)
        # print(cms_data)

    except Exception as e:
        with open(output, 'w') as file:
            file.truncate(0)

    return render(request, "cms_finger.html", locals())


def pushplus(request):
    if not request.user.username:
        # 没有登录
        return redirect("/login/")
    return render(request, "pushplus.html")

def helpdoc(request):
    if not request.user.username:
        # 没有登录
        return redirect("/login/")
    return render(request, "helpdoc.html")



def attack_time(request):
    with open('app01/json/logTime.json', 'r', encoding="utf-8") as f_json:
        timejson = json.load(f_json)
        # print(timejson)
    return JsonResponse(timejson)


def attack_event(request):
    with open('app01/json/findip.json', 'r', encoding="utf-8") as f_json:
        findipjson = json.load(f_json)

    result_list = findipjson['result']
    result_json = []

    for result in result_list:
        old_time_str = result[4]
        old_time_obj = datetime.strptime(old_time_str, '%d/%b/%Y:%H:%M:%S')
        new_time_str = old_time_obj.strftime('%Y-%m-%d %H:%M:%S')

        result_json.append({
            'ip': result[0],
            'location': result[2],
            'country': result[3],
            'time': new_time_str,
            'protocol': result[5],
            'port': result[6],
            'type': result[7]
        })
    # 将JSON数组打印出来
    json_data = json.dumps(result_json, indent=2)
    # print(json_data)
    # print(type(json_data))

    # 将数据转换为DataFrame对象
    path_data = json.loads(json_data)
    df = pd.DataFrame(path_data)
    # 将数据保存为Excel文件
    data_path = "E:/djangoProject/网络威胁情报自主监测平台/CTIM_System/api/tools/Data_storage/log_data.xlsx"
    df.to_excel(data_path, index=False)

    return JsonResponse(json_data, safe=False)

def event_radar(request):
    with open('app01/json/logEvent.json', 'r', encoding="utf-8") as f_json:
        event_json = json.load(f_json)
    return JsonResponse(event_json)
