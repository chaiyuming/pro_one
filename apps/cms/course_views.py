from django.views.generic import View
from django.shortcuts import render
from apps.course.models import CourseTeacher,CorseCategory,PubCourse,teacherCategory
from .forms import addCourseForm,CourseCategoryForm,TeacherForm,TeacherCategoryForm,TeacherListEditForm
# restful是用来返回json数据，直接将code/message/data封装成了一个模块，直接调用就可以，
#JsonResponse也可以返回json的字符串，但是每次都要将里面的参数手动写一遍
from utils import restful
from django.utils.decorators import method_decorator
from apps.pro_one_auth.decorators import xfz_permissoin_required
from django.views.decorators.http import require_POST,require_GET
import qiniu
from django.db.models import Q
# 发布课程
@method_decorator(xfz_permissoin_required(PubCourse),name='dispatch')
class PubCourses(View):
    def get(self,request):
        context={
            'categories':CorseCategory.objects.all(),
            'teachers':CourseTeacher.objects.all()
        }
        return render(request,'cms/pub_course.html',context=context)
    # post方式提交需要在form表单验证
    def post(self,request):
        form=addCourseForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data.get('title')
            video_url=form.cleaned_data.get('video_url')
            cover_url=form.cleaned_data.get('cover_url')
            price=form.cleaned_data.get('price')
            profile=form.cleaned_data.get('profile')
            category_id=form.cleaned_data.get('category_id')
            category=CorseCategory.objects.get(pk=category_id)
            teacher_id=form.cleaned_data.get('teacher_id')
            teacher=CourseTeacher.objects.get(pk=teacher_id)
            durarion=form.cleaned_data.get('durarion')
            PubCourse.objects.create(title=title,video_url=video_url,cover_url=cover_url,price=price,profile=profile,category=category,teacher=teacher,durarion=durarion)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_error())

# 课程分类
def course_category(request):
    categories=CorseCategory.objects.all()
    context={
        'categories':categories
    }
    return render(request,'cms/course_category.html',context=context)
# 添加分类
@require_POST
def add_course_category(request):
    category_name=request.POST.get('category_name')
    exist=CorseCategory.objects.filter(name=category_name).exists()
    if not exist:
        CorseCategory.objects.create(name=category_name)
        return restful.ok()
    else:
        return restful.params_error(message='该分类已经存在')

#课程分类编辑按钮
@require_POST
def edit_course_category(request):
    form=CourseCategoryForm(request.POST)
    if form.is_valid():
        pk=form.cleaned_data.get('pk')
        name=form.cleaned_data.get('name')
        CorseCategory.objects.filter(pk=pk).update(name=name)
        print('===========haha')
        return restful.ok()
    else:
        return restful.params_error(message=form.get_error())

# 课程分类删除按钮
@require_POST
def delete_course_category(request):
    pk=request.POST.get('pk')
    CorseCategory.objects.filter(pk=pk).delete()
    return restful.ok()


# 添加教师函数
class TeacherView(View):
    def get(self,request):
        categories=teacherCategory.objects.all()
        return render(request,'cms/add_teacher.html',context={
            'categories':categories
        })
    def post(self,request):
        form=TeacherForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            jobtitle=form.cleaned_data.get('jobtitle')
            profile=form.cleaned_data.get('profile')
            avatar=form.cleaned_data.get('avatar')
            category_id=form.cleaned_data.get('category')
            category=teacherCategory.objects.get(pk=category_id)
            CourseTeacher.objects.create(username=username,jobtitle=jobtitle,profile=profile,avatar=avatar,category=category)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_error())
# 上传图片只能用get方式
# @require_GET
# def teacher_token(request):
#     access_key = '5ixiJHJFv_euNuH47dr2SCN4wWcGOyJA7RDVKEHt'
#     secret_key = 'FMfUTWJwPkyGkJkQMb2fA_Dy1E2OASYETUs6TThC'
#     q=qiniu.Auth(access_key,secret_key)
#     bucket='cym-1991'
#     token=q.upload_token(bucket)
#     return restful.result(data={'token':token})

# 教师分组
def teacher_category(request):
    teacher_categories=teacherCategory.objects.all()
    context={
        'teacher_categories':teacher_categories
    }
    return render(request,'cms/teacher_category.html',context=context)

# 教师分组中添加分组按钮。
@require_POST
def add_teacher_category(request):
    group_name=request.POST.get('group_name')
    exist=teacherCategory.objects.filter(name=group_name).exists()
    if not exist:
        teacherCategory.objects.create(name=group_name)
        print('=============')
        return restful.ok()
    else:
        return restful.params_error(message='该分组已经存在')

# # 教师分组中编辑按钮后端代码
@require_POST
def edit_teacher_category(request):
    form=TeacherCategoryForm(request.POST)
    if form.is_valid():
        pk=form.cleaned_data.get('pk')
        name=form.cleaned_data.get('name')
        try:
            teacherCategory.objects.filter(pk=pk).update(name=name)
            return restful.ok()
        except:
            return restful.params_error(message='该分类不存在')
    else:
        return restful.params_error(data=form.get_error())
# # 教师分组中删除按钮后端代码
@require_POST
def delete_teacher_group(request):
    pk=request.POST.get('pk')
    teacherCategory.objects.filter(pk=pk).delete()
    return restful.ok()

# 教师列表添加了搜索功能
class TeacherList(View):
    def get(self,request):
        courseteachers=CourseTeacher.objects.all()
        groups=teacherCategory.objects.all()
        title=request.GET.get('title')
        print('==============')
        print(title)
        group_id=int(request.GET.get('group',0))
        if title and title !='None':
            courseteachers=courseteachers.filter(Q(username__contains=title) | Q(jobtitle__contains=title))
            # courseteachers=courseteachers.filter(username__contains=title)
        if group_id !=0:
            courseteachers=courseteachers.filter(category=group_id)
        context={
            'group_id':group_id,
            'title':title,
            'courseteachers':courseteachers,
            'groups':groups
        }
        return render(request,'cms/teacher_list.html',context=context)
# 教师列表编辑按钮
class TeacherListEdit(View):
    def get(self,request):
        pk=request.GET.get('pk')
        categories=teacherCategory.objects.all()
        teachers=CourseTeacher.objects.get(pk=pk)
        return render(request,'cms/add_teacher.html',context={
            'categories':categories,
            'teachers':teachers
        })
    def post(self,request):
        form=TeacherListEditForm(request.POST)
        if form.is_valid():
            pk=form.cleaned_data.get('pk')
            username = form.cleaned_data.get('username')
            jobtitle = form.cleaned_data.get('jobtitle')
            profile = form.cleaned_data.get('profile')
            avatar = form.cleaned_data.get('avatar')
            category_id = form.cleaned_data.get('category')
            category = teacherCategory.objects.get(pk=category_id)
            CourseTeacher.objects.filter(pk=pk).update(username=username, jobtitle=jobtitle, profile=profile, avatar=avatar,category=category)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_error())

# 删除某个教师列表
def delete_teacher_list(request):
    pk=request.POST.get('pk')
    CourseTeacher.objects.filter(pk=pk).delete()
    return restful.ok()


