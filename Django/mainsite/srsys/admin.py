"""
    made by Ian in 2017-8-17 14:38:57
    管理员界面
"""
from django.contrib import admin
from .models import Student,Advert

class StudentAdmin(admin.ModelAdmin):
    search_fields = ('stu_num','name') # 搜索框
    list_display_links = ('stu_num','name') # 标题列表
    list_display = ('stu_num','name','color','sketch','linedraw','total')

class AdvertAdmin(admin.ModelAdmin):
    list_display_links = ('advert_num','advert_url')
    list_display = ('advert_num', 'advert_url')

admin.site.register(Student,StudentAdmin)
admin.site.register(Advert,AdvertAdmin)