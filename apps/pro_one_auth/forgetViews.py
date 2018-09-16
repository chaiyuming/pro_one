from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from utils.captcha.hycaptcha import Captcha
from utils import restful
from utils.aliyunsdk import aliyun
from .models import User
from .forms import ForgetPasswordForm, ModifyPasswordForm
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import logout
import random


# 短信验证页面
class forgetPassword(View):
    def get(self, request):
        return render(request, 'pro_one_auth/forgetPassword.html')

    def post(self, request):
        form = ForgetPasswordForm(request.POST)
        if form.is_valid() and form.validate_data(request):
            telephone = form.cleaned_data.get('telephone')
            sms_captcha = form.cleaned_data.get('sms_captcha')
            print('telephone:%s' % telephone)
            print('sms_captcha:%s' % sms_captcha)
            # .first()获取到第一个数据，而不是queryset对象
            user = User.objects.filter(telephone=telephone).first()
            logout(request)
            return restful.result(data={"user_id": user.id})
            # return restful.result(data={'user_id':user.telephone})
            # return redirect(reverse('pro_one_auth:modifypassword'))
        else:
            message = form.get_error()
            print(message)
            return restful.params_error(message=message)


# 获取短信验证码
def rest_pwd(request):
    telephone = request.GET.get('telephone')
    if telephone:
        code=random.randrange(100000,999999)
        # code = Captcha.gene_text()
        print('短信验证码:%s' % code)
        # result=aliyun.send_sms(telephone,code=code)
        # 再短信发送之前先将短信保存在session中
        request.session['sms_captcha'] = code
        return HttpResponse('success')


# 修改密码
class ModifyPassword(View):
    def get(self, request):
        pk = request.GET.get('pk')
        # print(pk)
        user = User.objects.filter(pk=pk).first()
        # print(user)
        context = {
            'user': user
        }
        # 剩下的就是post改密码  要是有set_password 修改 如果是password=newpassword 保存的是明文密码
        return render(request, 'pro_one_auth/modifyPassword.html', context=context)
        # return render(request,'pro_one_auth/modifyPassword.html')
    def post(self, request):
        form = ModifyPasswordForm(request.POST)
        # telephone=request.POST.get('telephone')
        pk = request.POST.get('pk')
        if form.is_valid() and form.validate_data(request):
            # pk=form.cleaned_data.get('pk')
            password = form.cleaned_data.get('password')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.save()
            return restful.ok()
        else:
            message = form.get_error()
            return restful.params_error(message=message)
