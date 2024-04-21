from django.db import models
from django.contrib.auth.models import AbstractUser


# 用户表
class UserInfo(AbstractUser):
    nid = models.AutoField(primary_key=True)
    nick_name = models.CharField(max_length=16, verbose_name='昵称', null=True, blank=True)
    tel = models.CharField(verbose_name='手机号', max_length=12, null=True, blank=True)
    integral = models.IntegerField(default=20, verbose_name='用户积分')
    token = models.CharField(verbose_name="TOKEN", max_length=64, null=True, blank=True)

    class Meta:
        verbose_name_plural = '用户'
