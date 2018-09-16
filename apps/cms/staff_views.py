from django.shortcuts import render,redirect,reverse
from apps.pro_one_auth.models import User
from django.db.models import Q
from django.views.generic import View
from django.contrib.auth.models import Group
from apps.pro_one_auth.decorators import xfz_staff_required
from django.utils.decorators import method_decorator
from utils import restful
from django.http import HttpResponse
from django.contrib import messages

@xfz_staff_required
def staff(request):
    staffs=User.objects.filter(Q(is_staff=True) | Q(is_superuser=True))
    context={
        'staffs':staffs
    }
    return render(request,'cms/staff.html',context=context)
@method_decorator(xfz_staff_required,name='dispatch')
class AddStaff(View):
    def get(self,request):
        groups=Group.objects.all()
        context={
            'groups':groups
        }
        return render(request,'cms/add_staff.html',context=context)
    def post(self,request):
        # 得到input标签name值为telephone的值
        telephone=request.POST.get('telephone')
        staffs=User.objects.filter(Q(is_staff=True) | Q(is_superuser=True))
        exist=staffs.filter(telephone=telephone).exists()
        if not exist:
            user=User.objects.get(telephone=telephone)
            user.is_staff=True
            # 查找用户拥有的所有的权限
            group_ids=request.POST.getlist('groups')
            # 找到员工对应的id
            group_id=Group.objects.filter(pk__in=group_ids)
            # 将用户和权限绑定
            user.groups.set(group_id)
            user.save()
            # return restful.ok()
            return redirect(reverse("cms:staff"))
        else:
            print('该号码已在员工列表中')
            messages.info(request,'该号码已在员工列表中')
            return redirect(reverse('cms:add_staff'))
            # return restful.params_error(message='该号码已在员工列表中')
            # return HttpResponse('该号码已在员工列表中')



def DeleteStaff(request):
    telephone=request.POST.get('telephone')
    user = User.objects.get(telephone=telephone)
    user.is_staff = False
    user.save()
    print('===========')
    print(telephone)
    print('===========')
    return restful.ok()





