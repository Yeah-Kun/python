"""
    made by Ian in 2017-8-17 14:39:42
    学生信息模型层
"""
from django.db import models

class Student(models.Model):
    class Meta:
        verbose_name = "考生信息"
        verbose_name_plural = "考生分数"

    stu_num = models.CharField(max_length=10, verbose_name="考生号")
    name = models.CharField(max_length=10, verbose_name="姓名")
    color = models.IntegerField(verbose_name="色彩")
    sketch = models.IntegerField(verbose_name="速写")
    linedraw = models.IntegerField(verbose_name="素描")
    total = models.IntegerField(verbose_name="总分")

class Advert(models.Model):
    class Meta:
        verbose_name = "广告"
        verbose_name_plural = "广告"

    img = models.ImageField("广告图片(尺寸:325px*45px)", upload_to="update")
    advert_url = models.URLField(verbose_name="广告链接")
    advert_num = models.IntegerField(verbose_name="广告序号")