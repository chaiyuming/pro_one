from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group,Permission,ContentType
from apps.news.models import News,NewsCategory,Banner,Comment
from apps.course.models import PubCourse,CourseOrder,CourseTeacher,CorseCategory
from apps.payinfo.models import PayinfoModel,payinfoOrder

class Command(BaseCommand):
    def handle(self, *args, **options):
        # get_for_model(model)参数为一个其他model的 class 类或者实例，返回content type的实例
        # 编辑人员权限:编辑文章/轮播图/付费资讯/课程
        edit_content_type=[
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewsCategory),
            ContentType.objects.get_for_model(Banner),
            ContentType.objects.get_for_model(Comment),
            ContentType.objects.get_for_model(PubCourse),
            ContentType.objects.get_for_model(CorseCategory),
            ContentType.objects.get_for_model(CourseTeacher),
            ContentType.objects.get_for_model(PayinfoModel)
        ]
        edit_permissions=Permission.objects.filter(content_type__in=edit_content_type)
        editGroup=Group.objects.create(name='编辑组')
        editGroup.permissions.set(edit_permissions)
        # 财务组权限
        finance_content_type=[
            ContentType.objects.get_for_model(payinfoOrder),
            ContentType.objects.get_for_model(CourseOrder)
        ]
        finance_permissions=Permission.objects.filter(content_type__in=finance_content_type)
        financeGroup=Group.objects.create(name='财务组')
        financeGroup.permissions.set(finance_permissions)
        # 管理员权限:拥有编辑和财务组的权限
        # edit_permissions.union(finance_permissions),.union()将edit_permissions.union和finance_permission合二为一
        admin_permission=edit_permissions.union(finance_permissions)
        adminGroup=Group.objects.create(name='管理员')
        adminGroup.permissions.set(admin_permission)

        self.stdout.write(self.style.SUCCESS('权限初始化成功！'))


