"""
    made by Ian in 2017-8-17 14:39:42
    学生信息模型层
"""
from django.db import models

class Student(models.Model):
    class Meta:
        verbose_name = "考生信息"
        verbose_name_plural = "分数数据库"

    stu_num = models.CharField(max_length=10, verbose_name="考生号")
    name = models.CharField(max_length=10, verbose_name="姓名")
    color = models.IntegerField(verbose_name="色彩")
    sketch = models.IntegerField(verbose_name="速写")
    linedraw = models.IntegerField(verbose_name="素描")
    total = models.IntegerField(verbose_name="总分")

