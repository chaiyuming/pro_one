from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager,User
from django.db import models

class UserManger(BaseUserManager):
    def _create_user(self,telephone,username,password,**kwargs):
        # self.model就相当于User
        user = self.model(telephone=telephone, username=username, **kwargs)
        # password需要通过set_password方式去设置
        user.set_password(password)
        user.save()
        return user
    def create_user(self,telephone,username,password,**kwargs):
        # 当前创建的只是普通用户，所以得先把is_superuser传给kwargs并赋值为False
        kwargs['is_superuser']=False
        return self._create_user(telephone,username,password,**kwargs)
    def create_superuser(self,telephone,username,password,**kwargs):
        kwargs['is_superuser']=True
        return self._create_user(telephone,username,password,**kwargs)

# 自定义User模型
class User(AbstractBaseUser,PermissionsMixin):
    telephone=models.CharField(max_length=11,unique=True)
    username=models.CharField(max_length=110)
    email=models.EmailField(unique=True,null=True)
    gender=models.IntegerField(default=0)
    date_join=models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    # USERNAME_FIELD:这个属性是以后在使用authenticate时进行验证的字段
    USERNAME_FIELD='telephone'
    #这个属性使用来，以后在命令行中使用createsuperuser命令的时候会让你输入的字段
    REQUIRED_FIELDS = ['username']
    #以后给某个用户发送邮箱的时候就会使用这个属性指定的字段的值来发送。
    EMAIL_FIELD='email'

    objects=UserManger()

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username