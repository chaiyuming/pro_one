from django import forms
from django.shortcuts import reverse ,redirect
from django.contrib import messages
from .models import User
from apps.forms import FormMixin
from utils import restful
#用来验证登录信息
class LoginForm(forms.Form):
    telephone=forms.CharField(min_length=11,max_length=11,error_messages={
        'required':'必须放入11位手机号码',
        'min_length':'手机号码必须为11位',
        'max_length':'手机号码必须为11位',
    })
    password=forms.CharField(min_length=6,max_length=20,error_messages={
        'required':'必须填入密码',
        'min_length':'密码长度不能少于6位',
        'max_length':'密码长度不能大于20位',
    })
    remember=forms.IntegerField(required=False)

class RegisterForm(forms.Form,FormMixin):
    '''
    表达某种校验的参数必须和ajax中data中的key对应，不然会有错。
    '''
    telephone=forms.CharField(min_length=11,max_length=11,error_messages={
        'required':'必须放入11位手机号码',
        'min_length':'手机号码必须为11位',
        'max_length':'手机号码必须为11位',
    })
    username=forms.CharField(max_length=20,min_length=4,error_messages={
        'required':'必须输入用户名',
        'min_length': "用户名不能少于4个字符",
        'max_length': "用户名不能大于20个字符",
    })
    password=forms.CharField(min_length=8,max_length=20,error_messages={
        'required':"必须填入密码",
        'min_length':"密码长度不能少于8",
        'max_length':"密码长度不能大于20",
    })
    password_repeat=forms.CharField(min_length=8,max_length=20,error_messages={
        'required':"请重复输入密码",
        'min_length':"密码长度不能少于8",
        'max_length':"密码长度不能大于20",
    })
    sms_captcha=forms.CharField(max_length=4,min_length=4,error_messages={
        'required':"请输入四位数字的短信验证码",
    })
    img_captcha=forms.CharField(min_length=4,max_length=4,error_messages={
        'required':"请输入图形验证码",
    })
#定义验证函数，就是当调用views.py中的is_valid时，系统能自动调用clean方法
    def validate_data(self,request):
        #重写cleaned_date方法
        cleaned_data=self.cleaned_data
        password=cleaned_data.get('password')
        password_repeat=cleaned_data.get('password_repeat')

        if password !=password_repeat:
            return self.add_error('password','两次密码输入不一致!')
            # messages.info(request,'两次密码输入不一致！')
            # return redirect(reverse('pro_one_auth:register'))


        sms_captcha=cleaned_data.get('sms_captcha')
        sever_sms_captcha=request.session.get('sms_captcha')
        if sms_captcha.lower() != sever_sms_captcha.lower():
            # messages.info(request,'短信验证码不一致!')
            # return redirect(reverse('pro_one_auth:register'))
            return self.add_error('sms_captcha','短信验证码不一致!')

        img_captcha=cleaned_data.get('img_captcha')
        sever_img_captcha=request.session.get('img_captcha')
        if img_captcha.lower() != sever_img_captcha.lower():
            # messages.info(request,'验证码错误')
            # return redirect(reverse('pro_one_auth:register'))
            return self.add_error('img_captcha','验证码错误')

        #验证用户是否已经注册
        telephone=cleaned_data.get('telephone')
        exist=User.objects.filter(telephone=telephone).exists()
        if exist:
            # messages.info(request,'该手机号码已经注册')
            # return redirect(reverse('pro_one_auth:register'))
            return self.add_error('telephone','该手机号码已经注册')
        return True

# 忘记密码
class ForgetPasswordForm(forms.Form,FormMixin):
    telephone = forms.CharField(min_length=11, max_length=11, error_messages={
        'required': '必须放入11位手机号码',
        'min_length': '手机号码必须为11位',
        'max_length': '手机号码必须为11位',
    })
    sms_captcha = forms.IntegerField(error_messages={
        'required': "请输入六位数字的短信验证码",
    })
#定义验证函数，就是当调用views.py中的is_valid时，系统能自动调用clean方法
    def validate_data(self,request):
        # 重写cleaned_date方法
        cleaned_data = self.cleaned_data
        sms_captcha = cleaned_data.get('sms_captcha')
        sever_sms_captcha = request.session.get('sms_captcha')
        if sms_captcha != sever_sms_captcha:
            # messages.info(request,'短信验证码不一致!')
            # return redirect(reverse('pro_one_auth:register'))
            return self.add_error('sms_captcha', '短信验证码不一致!')
        # 验证用户是否已经注册
        telephone = cleaned_data.get('telephone')
        exist = User.objects.filter(telephone=telephone).exists()
        if not exist:
            # messages.info(request,'该手机号码已经注册')
            # return redirect(reverse('pro_one_auth:register'))
            return self.add_error('telephone', '该手机号码不存在，请检查手机号码是否错误或者是否注册')
        return True

# 修改密码表单验证
class ModifyPasswordForm(forms.Form,FormMixin):
    # telephone = forms.CharField()
    # pk=forms.IntegerField()
    password = forms.CharField(min_length=8, max_length=20, error_messages={
        'required': "必须填入密码",
        'min_length': "密码长度不能少于8",
        'max_length': "密码长度不能大于20",
    })
    repeat_password = forms.CharField(min_length=8, max_length=20, error_messages={
        'required': "请重复输入密码",
        'min_length': "密码长度不能少于8",
        'max_length': "密码长度不能大于20",
    })
    def validate_data(self, request):
        # 重写cleaned_date方法
        cleaned_data = self.cleaned_data
        password = cleaned_data.get('password')
        repeat_password = cleaned_data.get('repeat_password')
        if password != repeat_password:
            return self.add_error('password', '两次密码输入不一致!')
            # messages.info(request,'两次密码输入不一致！')
            # return redirect(reverse('pro_one_auth:register'))
        return True




