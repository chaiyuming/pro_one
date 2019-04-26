from functools import wraps
from django.contrib.auth.models import Permission,ContentType
from django.http import Http404
from django.shortcuts import render,redirect
from utils import restful

def xfz_login_required(viewfunc):
    @wraps(viewfunc)
    def _wrapper(request,*args,**kwargs):
        if request.user.is_authenticated:
            return viewfunc(request,*args,**kwargs)
        else:
            if request.is_ajax():
                return restful.params_error(message='请先登录')
            else:
                return redirect('/')
    return _wrapper



# 组用户权限
def xfz_permissoin_required(model):
    def decorator(viewfunc):
        @wraps(viewfunc)
        def _wrapper(request,*args,**kwargs):
            # 获取模型的所有权限
            content_type=ContentType.objects.get_for_model(model)
            permissions=Permission.objects.filter(content_type=content_type)
            # has_perm判断用户拥有哪个权限,只能采用字符串的形式来判断
            # 字符串的形式为：app_label.codename   codename为权限的名字
            code_name=[content_type.app_label+'.'+permission.codename for permission in permissions]
            print('=' * 20)
            result=request.user.has_perms(code_name)
            print('+'*10)
            print(result)
            print('+'*10)
            if result:
                return viewfunc(request,*args,**kwargs)
            else:
                raise Http404()
        return  _wrapper
    return decorator
#超级用户权限
def xfz_staff_required(viewfunc):
    @wraps(viewfunc)
    def _wrapper(reuqest,*args,**kwargs):
        if reuqest.user.is_superuser:
            return viewfunc(reuqest,*args,**kwargs)
        else:
            raise Http404
    return _wrapper


