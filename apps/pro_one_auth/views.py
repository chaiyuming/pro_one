from django.shortcuts import render,redirect,reverse
from .forms import LoginForm,RegisterForm
from django.contrib.auth import authenticate,login,logout
from django.views.generic import View
# 导入自带消息模块。
from django.contrib import messages
from utils.captcha.hycaptcha import Captcha
from io import BytesIO
from django.http import HttpResponse
from utils.aliyunsdk import aliyun
from .models import User
from utils import restful
class LoginView(View):
    def get(self,request):
        return render(request,'pro_one_auth/login.html')
    def post(self,request):
        form=LoginForm(request.POST)
        if form.is_valid():
            telephone=form.cleaned_data.get('telephone')
            password=form.cleaned_data.get('password')
            remember=form.cleaned_data.get('remember')
            user=authenticate(request,username=telephone,password=password)
            print(telephone)
            print(password)
            # 这个用户存在数据库中
            if user:
                if user.is_active:
                    login(request,user)
                # nexturl=request.GET.get('next')
                # if nexturl:
                #     return redirect(nexturl) 
                    if remember:
                        request.session.set_expiry(None)
                    #     设置过期时间，None表示默认的过期时间，2个星期；0表示关闭浏览器就结束
                    else:
                        request.session.set_expiry(0)
                    return redirect(reverse('news:index'))
            else:
                messages.info(request,'用户名或密码错误')
                return redirect(reverse('pro_one_auth:LoginView'))
        else:
            messages.info(request,'用户不存在，请注册！')
            return redirect(reverse('pro_one_auth:LoginView'))
#Form表单版本的注册代码
# class RegisterView(View):
#     def get(self,request):
#         return render(request,'pro_one_auth/register.html')
#     def post(self,request):
#         form=RegisterForm(request.POST)
#         if form.is_valid() and form.validate_data(request):
#             telephone=form.cleaned_data.get('telephone')
#             username=form.cleaned_data.get('username')
#             password=form.cleaned_data.get('password')
#             user=User.objects.create_user(telephone=telephone,username=username,password=password)
#             #将注册信息保存到User后自动登入。
#             login(request,user)
#             return redirect(reverse('news:index'))
#         else:
#             message=form.get_error()
#             messages.info(request,message)
#             return redirect(reverse('pro_one_auth:register'))

# ajax请求版本的注册代码
class RegisterView(View):
    def get(self,request):
        return render(request,'pro_one_auth/register.html')
    def post(self,request):
        form=RegisterForm(request.POST)
        if form.is_valid() and form.validate_data(request):
            #切记.py文件每个语句后不能逗号
            telephone=form.cleaned_data.get('telephone')
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            print("手机号码：%s" % telephone)
            user=User.objects.create_user(telephone=telephone,username=username,password=password)
            login(request,user)
            return restful.ok()
        else:
            message=form.get_error()
            print(message)
            return restful.params_error(message=message)
def LogoutView(request):
    logout(request)
    return redirect('/')
def img_captcha(request):
    text,image=Captcha.gene_code()
    #image不是一个httpresponse可以识别的对象，因此先要将image变成一个数据流才能放到Httpresponse中，
    #BytesIO相当于一个管道可以用来储存字节流
    out=BytesIO()
    image.save(out,'png')
    #将文件指针设置到0的位置
    out.seek(0)
    # content_type指定数据的类型为image类型
    response=HttpResponse(content_type='image/png')
    # out.read()表示从out中读取内容
    response.write(out.read())
    response['Content-length'] = out.tell()
    # 在图形验证码发送之前，现将其保存在session中
    request.session['img_captcha']=text
    return response
def sms_captcha(request):
    # 调用 utils/captcha/hycaptcha.py中的Captcha.gene_text()函数
    telephone = request.GET.get('telephone')
    code=Captcha.gene_text()
    # result=aliyun.send_sms(telephone,code=code)
    print('短信验证码：%s'%code)
    # 再短信发送之前先将短信保存在session中
    request.session['sms_captcha']=code
    return HttpResponse('success')
