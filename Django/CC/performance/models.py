'''
	模型层
	create by Ian in 2017-11-30 20:49:13 
'''
from django.db import models

# Create your models here.

class Student(models.Model):
	'''学生信息模型层'''
	name = models.CharField(max_length=30)
	
