"""
    made by Ian in 2017-8-17 19:22:52
    业务逻辑层
"""
from django.shortcuts import render
from django.http import HttpResponse
from srsys.models import Student
from srsys.utils import VerifyCode
from io import BytesIO
from srsys.models import Advert

def index(request):
    """查询页面"""
    ctx = {}
    Advert_1 = Advert.objects.get(advert_num=1)  # 广告1
    Advert_2 = Advert.objects.get(advert_num=2)  # 广告2

    ctx['Adverturl1'] = Advert_1.advert_url
    ctx['Adverturl2'] = Advert_2.advert_url
    ctx['Advertimg1'] = str(Advert_1.img)
    ctx['Advertimg2'] = str(Advert_2.img)
    return render(request, 'srsys/index.html',ctx)


def result(request):
    """成绩页面"""
    ctx = {}
    Advert_1 = Advert.objects.get(advert_num=1)  # 广告1
    Advert_2 = Advert.objects.get(advert_num=2)  # 广告2

    ctx['Adverturl1'] = Advert_1.advert_url
    ctx['Adverturl2'] = Advert_2.advert_url
    ctx['Advertimg1'] = str(Advert_1.img)
    ctx['Advertimg2'] = str(Advert_2.img)
    if request.POST['InputStuNum']!='请输入十位考生号' or request.POST['InputName']!='请输入考生姓名':
        if request.POST['InputVerifyCode'] == request.session.get('check_code'): # 判断输入的验证码与session里面的是否一致
            try:
                Datebase_Return = Student.objects.get(stu_num__exact=(request.POST['InputStuNum']),
                                                         name__exact=(request.POST['InputName']))
                ctx['studentnum'] = Datebase_Return.stu_num
                ctx['name'] = Datebase_Return.name
                ctx['color'] = Datebase_Return.color
                ctx['sketch'] = Datebase_Return.sketch
                ctx['linedraw'] = Datebase_Return.linedraw
                ctx['total'] = Datebase_Return.total
                return render(request, 'srsys/result.html',ctx)

            except:
                ctx['ErrorMessage'] = u'账号或密码输入错误，请重新输入！'
        else:
            ctx['ErrorMessage'] = u'验证码有误，请重新输入！'
    else:
        ctx['ErrorMessage'] = u'信息未完整输入！'
    return render(request, 'srsys/index.html', ctx)

def create_code_img(request):
    """在内存中开辟空间用以生成临时的图片"""
    f = BytesIO()
    size = (83,30)
    img,code = VerifyCode.create_code(size)
    request.session['check_code'] = code  # 将验证码存在服务器的session中，用于校验
    img.save(f,'jpeg')
    return HttpResponse(f.getvalue())