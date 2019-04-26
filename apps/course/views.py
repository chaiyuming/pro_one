from django.shortcuts import render,reverse,redirect
from django.http import HttpResponse
from .models import PubCourse,CorseCategory,CourseTeacher,CourseOrder
from django.conf import settings
import os,hashlib,hmac,time
from utils import restful
from hashlib import md5
# 导入关闭视图函数的csrf_token
from django.views.decorators.csrf import  csrf_exempt


# Create your views here.

def course_index(request):
    courses=PubCourse.objects.all()
    context={
        'courses':courses
    }
    return render(request,'course/course_index.html',
                  context=context)

def course_detail(request,course_id):
    course = PubCourse.objects.get(pk=course_id)
    # exists()表示满足当前条件的数据是否存在
    isbuyed = CourseOrder.objects.filter(order_name=course, buyer=request.user, status=2).exists()
    context = {
        'course': course,
        'isbuyed':isbuyed
    }
    return render(request,'course/course_detail.html',context=context)

# 视频播放后台代码设置
def course_token(request):
    # video为自己定义的
    # 获取视频的链接地址，相当于videourl=http://ignpqx46eyffb2tr29p.exp.bcevod.com/mda-ignq5aygr8x76ai7/mda-ignq5aygr8x76ai7.m3u8
    video_url=request.GET.get('video')
    course_id=request.GET.get('courseid')
    print('===========')
    print(course_id)
    print('===========')
    isbuyed=CourseOrder.objects.filter(order_name=course_id,buyer=request.user,status=2).exists()
    if not isbuyed:
        return restful.params_error(message='请先购买课程！')
    # 设置过期时间，time.time()为当前时间；单位s
    expiration_time=int(time.time())+2*60*60

    # 获取USER_ID和USER_KEY
    USER_ID=settings.BAIDU_CLOUD_USER_ID
    USER_KEY=settings.BAIDU_CLOUD_USER_KEY
    # splitext分离文件名与扩展名；默认返回(fname,fextension)元组，可做分片操作
    # os.path.splitext('c:\\csv\\test.csv') >>>('c:\\csv\\test', '.csv')
    extension=os.path.splitext(video_url)[1]
    # 最终结果得到的是mda-ignq5aygr8x76ai7
    media_id=video_url.split('/')[-1].replace(extension,'')

    # 生成签名（signature）的过程
    # 将USER_KEY通过.encode()转化为Bytes类型。
    key=USER_KEY.encode('utf-8')
    message='/{0}/{1}'.format(media_id,expiration_time).encode('utf-8')
    signature=hmac.new(key,message,digestmod=hashlib.sha256).hexdigest()
    # 生成token
    token='{0}_{1}_{2}'.format(signature,USER_ID,expiration_time)
    # 将成成的token返回,提供给前端，前端只有获取了token才能播放视频。
    return  restful.result(data={'token':token})

# 课程订单
def course_order(request):
    # .get('course_id')已经绑定在了购买可能按钮上。
    course_id=request.GET.get('course_id')
    course=PubCourse.objects.get(pk=course_id)
    print('==========')
    print(course)
    print('==========')
    # 跳转到支付界面时，自动创建一个课程订单
    order=CourseOrder.objects.create(amount=course.price,order_name=course,status=1,buyer=request.user,)
    # 在课程订单中判断该课程是否已经购买，如果已经购买了就返回到课程的详细页面
    isbuyed=CourseOrder.objects.filter(order_name=course,buyer=request.user,status=2).exists()
    if isbuyed:
        return redirect(reverse('course:course_detail',kwargs={'course_id':course.pk}))
    context={
        'course':course,
        # .build_absolute_uri()可以获取一个完整的/notify_url/网址，拼接到域名的后面，比如http://154.8.146.47:8000/course/notify_url/
        'notify_url':request.build_absolute_uri(reverse('course:notify_url')),
        # 将'course:course_detail' course_id=course.pk 转换为网址传递到服务器，让前端获取
        # 付款以后跳转到该课程的详情页面
        'return_url':request.build_absolute_uri(reverse('course:course_detail',kwargs={'course_id':course.pk})),
        'order':order
    }
    return render(request,'course/course_order.html',context=context)
# 定义一个函数获取key
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
    print('goodsname:', goodsname)
    print('istype:', istype)
    print('notify_url:', notify_url)
    print('orderid:', orderid)
    print('price:', price)
    print('return_url:', return_url)
    print('token:', token)
    print('orderuid:', orderuid)
    # 通过md5加密，并按这个顺序拼接，最后通过.hexdigest()获取到这个值。
    # key=md5(goodsname+istype+notify_url+orderid+orderuid+price+return_url+token+uid).encode('utf-8').hexdigest()
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
    # 找到订单id
    order_id=request.POST.get('orderid')
    #将该订单支付状态改为已支付即=2
    CourseOrder.objects.filter(pk=order_id).update(status=2)
    print('status:',order_id)
    return restful.ok()




