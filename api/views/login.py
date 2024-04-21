from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django import forms
from django.contrib import auth
from app01.models import UserInfo
from django.views import View


# 登录注册字段的父类
class LoginBaseForm(forms.Form):
    name = forms.CharField(error_messages={"required": "请输入用户名"})
    pwd = forms.CharField(error_messages={"required": "请输入密码"})
    code = forms.CharField(error_messages={"required": "请输入验证码"})

    # 重写init方法
    def __init__(self, *args, **kwargs):
        # 做自己想做的事情
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    # 局部钩子
    def clean_code(self):
        code = self.cleaned_data.get('code')
        valid_code = self.request.session.get('valid_code')  # request请求 session中获取验证码
        if valid_code.upper() != code.upper():
            self.add_error("code", "验证码输入错误")
        return self.cleaned_data


# 登录的字段验证
class LoginForm(LoginBaseForm):
    def clean(self):
        name = self.cleaned_data.get('name')
        pwd = self.cleaned_data.get('pwd')

        user = auth.authenticate(username=name, password=pwd)  # 校验数据库中的字段成功后返回一个用户对象
        if not user or not user.check_password(pwd):
            try:
                # 尝试手动获取用户对象
                user = get_user_model().objects.get(username=name)
                if user.check_password(pwd):
                    if not user.is_active:
                        self.add_error(None, "用户未被激活，请联系管理员！")
                        return self.cleaned_data
                else:
                    raise get_user_model().DoesNotExist
            except get_user_model().DoesNotExist:
                # 用户登录校验不通过
                # 为指定的字段添加错误信息
                self.add_error("pwd", "用户名或密码错误")
                return self.cleaned_data

        # 把用户对象放到 cleaned_data 中
        self.cleaned_data['user'] = user
        return self.cleaned_data


# 注册字段验证
class SignForm(LoginBaseForm):
    re_pwd = forms.CharField(error_messages={"required": "请输入确认密码"})

    # 全局钩子
    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        re_pwd = self.cleaned_data.get('re_pwd')
        if re_pwd != pwd:
            self.add_error("re_pwd", "两次密码不一致")
        return self.cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get("name")
        user_query = UserInfo.objects.filter(username=name)
        if user_query:
            self.add_error("name", "该用户已注册")
        return self.cleaned_data


# 登录失败的可复用代码
def clean_form(form):
    err_dict: dict = form.errors
    # 拿到所有错误的字段名字
    err_valid = list(err_dict.keys())[0]
    # 拿到第一个字段的第一个错误信息
    err_msg = err_dict[err_valid][0]
    return err_valid, err_msg


# CBV模式
class LoginView(View):
    def post(self, request):
        if request.method == 'POST':
            res = {
                'code': 425,
                'msg': "登录成功!",
                'self': None
            }
            data = request.data  # 请求体

            form = LoginForm(data, request=request)
            if not form.is_valid():
                # 验证不通过
                res['self'], res['msg'] = clean_form(form)  # 接收错误字段和错误信息
                return JsonResponse(res)
            # 验证通过
            # 写我们的登录操作
            user = form.cleaned_data.get('user')
            auth.login(request, user)

            res['code'] = 0
            return JsonResponse(res)


class SignView(View):
    def post(self, request):
        res = {
            'code': 425,
            'msg': "登录成功!",
            'self': None
        }
        data = request.data
        form = SignForm(data, request=request)
        if not form.is_valid():
            # 验证不通过
            res['self'], res['msg'] = clean_form(form)  # 接收错误字段和错误信息
            return JsonResponse(res)

        # 注册成功的代码
        name = form.data.get('name')
        pwd = form.data.get('pwd')
        user = UserInfo.objects.create_user(username=name, password=pwd)
        user.is_active = False  # 设置默认为非激活状态
        user.save()

        # 注册之后直接登录
        # auth.login(request, user)
        res['msg'] = "注册信息已提交给管理员，等待审核成功后即可登录！"
        res['code'] = 0

        return JsonResponse(res)
