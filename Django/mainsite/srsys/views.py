"""
    made by Ian in 2017-8-17 19:22:52
    业务逻辑层
"""
from django.shortcuts import render

from srsys.models import Student

def index(request):
    return render(request, 'srsys/index.html')


def result(request):
    ctx = {}
    if request.POST:
        try:
            Datebase_Return = Student.objects.filter(stu_num=(request.POST['InputStuNum']),
                                                         name=(request.POST['InputName']))
            for var in Datebase_Return:
                ctx['studentnum'] = var.stu_num
                ctx['name'] = var.name
                ctx['color'] = var.color
                ctx['sketch'] = var.sketch
                ctx['linedraw'] = var.linedraw
                ctx['total'] = var.total
        except:
            ctx['ErrorMessage'] = u'账号或密码输入错误，请检查'

        return render(request, 'srsys/index.html',ctx)

    else:
        ctx['ErrorMessage'] = u'未输入完整'
        return render(request, 'srsys/index.html', ctx)

