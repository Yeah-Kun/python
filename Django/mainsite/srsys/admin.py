"""
    made by Ian in 2017-8-17 14:38:57
    管理员界面
"""
from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    search_fields = ('stu_num','name') # 搜索框
    list_display_links = ('stu_num','name') # 列表
    list_display = ('stu_num','name','color','sketch','linedraw','total')

admin.site.register(Student,)
