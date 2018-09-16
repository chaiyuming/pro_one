from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from .models import PayinfoModel,payinfoOrder
from django.views.decorators.csrf import csrf_exempt
from utils import restful
from hashlib import md5
from django.http import FileResponse
from django.conf import settings
import os


# Create your views here.

def payinfo_index(request):
    payinfoes=PayinfoModel.objects.all()
    orders=payinfoOrder.objects.all()
    context={
        'payinfoes':payinfoes,
        'orders':orders
    }
    return render(request,'payinfo/payinfo.html',context=context)



def payinfo_order(request):
    payinfo_id=request.GET.get('payinfo_id')
    print('==========')
    print(payinfo_id)
    print('==========')
    payinfo=PayinfoModel.objects.get(pk=payinfo_id)
    buyed=payinfoOrder.objects.filter(payinfo=payinfo,status=2,buyer=request.user).exists()
    if  buyed:
        # 果如已经购买了则跳转到下载的页面
        return redirect(reverse('payinfo:download_payinfo')+"?payinfo_id=%s"%payinfo.pk)
    order = payinfoOrder.objects.create(amount=payinfo.price, buyer=request.user, status=1, payinfo=payinfo)
    context={
        'payinfo':payinfo,
        'order':order,
        'notify_url':request.build_absolute_uri(reverse('payinfo:notify_url')),
        # 支付成功后跳转到下载地址
        'return_url':request.build_absolute_uri(reverse('payinfo:download_payinfo')+"?payinfo_id=%s"%payinfo.pk)
    }
    return render(request,'payinfo/create_order.html',context=context)
# 获取key
def order_key(request):
    goodsname = request.POST.get("goodsname")
    istype = request.POST.get("istype")
    notify_url = request.POST.get("notify_url")
    orderid = request.POST.get("orderid")
    price = request.POST.get("price")
    return_url = request.POST.get("return_url")

    token = 'e6110f92abcb11040ba153967847b7a6'
    # 客户编号
    orderuid = str(request.user.pk)
    uid = '49dc532695baa99e16e01bc0'
    # 通过md5加密，并按这个顺序拼接，最后通过.hexdigest()获取到这个值。
    key = md5((goodsname + istype + notify_url + orderid + orderuid + price + return_url + token + uid).encode(
        "utf-8")).hexdigest()
    print('key',key)
    # 将key以json格式返回
    return restful.result(data={'key':key})
# 定义一个函数获取通知回调网址
# 在django中如果需要将数据发送给视图函数用post方法，那么需要传递csrf_token,
# 关闭csrf_token
@csrf_exempt
def notify_url(request):
    order_id=request.POST.get('order_id')
    payinfoOrder.objects.filter(pk=order_id).update(status=2)
    return restful.ok()

#购买后附件下载
def download_payinfo(request):
    payinfo_id=request.GET.get('payinfo_id')
    payinfo=PayinfoModel.objects.get(pk=payinfo_id)
    buyed=payinfoOrder.objects.filter(payinfo=payinfo,buyer=request.user,status=2)
    if not buyed:
        return redirect(reverse('payinfo:payinfo_order'))
    # 找到payinfo的附件路径
    path=payinfo.path
    # 作为一个附件的形式下载，而不是普通的文件下载，那么需要导入FileResponse
    # 以读取二进制的形式读取文件，多个路径需要通过os.path.join()的形式进行拼接
    response=FileResponse(open(os.path.join(settings.MEDIA_ROOT,path),'rb'))
    # 需要作为附件的形式下载，必须写下面两句代码
    response['Content-Type']='image/jpg'
    # /20180728/xx.jpg/经过.spilt('/')变成['',20180728，xx.jpg],[-1]得到了xx.jpg
    response['Content-Disposition']="attachment;filename='%s'"%path.split('/')[-1]
    return response

