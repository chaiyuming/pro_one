from django.views.generic import View
from django.shortcuts import render
from apps.course.models import CourseTeacher,CorseCategory,PubCourse,teacherCategory
from .forms import addCourseForm,CourseCategoryForm,TeacherForm,TeacherCategoryForm,TeacherListEditForm,EditCourseListForm
from utils import restful
from datetime import datetime
from django.db.models import Q
from django.core.paginator import Paginator
# 可以对url进行编辑
from urllib import parse
from django.conf import settings
# 课程列表部分
class CourseList(View):
    def get(self,request):
        page=int(request.GET.get('p',1))
        courses=PubCourse.objects.select_related('teacher','category')
        categories=CorseCategory.objects.all()
        start=request.GET.get('start')
        end=request.GET.get('end')
        title=request.GET.get('title')
        category_id=int(request.GET.get('category',0))
        if start and end and start !='None' and end !='None':
            start_time=datetime.strptime(start,'%Y/%m/%d')
            end_time=datetime.strptime(end,'%Y/%m/%d')
            courses=courses.filter(pub_time__range=(start_time,end_time))
        if title and title != 'None':
            courses=courses.filter(Q(title__icontains=title) | Q(teacher__username__icontains=title))
        if category_id !=0:
            courses=courses.filter(category=category_id)

        # 创建对象
        paginator=Paginator(courses,2)
        pag_objects=paginator.page(page)
        data_pagination = self.get_data_pagination(paginator, pag_objects, count_pages=2)
        context={
            'paginator': paginator,
            'pag_objects': pag_objects,
            'categories':categories,
            'start':start,
            'end':end,
            'title':title,
            'category_id':category_id,
            # 返回某一页的对象值
            'courses': pag_objects.object_list,
            'url_parameter': parse.urlencode({
                'start': start,
                'end': end,
                'title': title,
                'category_id': category_id
            })
        }
        # 将data_pagination更新到context中，既可以去前端代码中去渲染
        context.update(data_pagination)
        return render(request,'add/course_list.html',context=context)
    def get_data_pagination(self,paginator,pag_objects,count_pages=2,):
        current_page=pag_objects.number
        total_pages=paginator.num_pages
        # 定义三个点，默认为false
        left_has_more=False
        right_has_more=False
        # 当前页左边
        if current_page <= count_pages+2:
            left_page=range(1,current_page)
        else:
            left_has_more=True
            left_page=range(current_page-count_pages,current_page)

        # 当前页右边
        if current_page >= total_pages-count_pages-1:
            right_page=range(current_page+1,total_pages+1)
        else:
            right_has_more=True
            right_page=range(current_page+1,current_page+count_pages+1)
        # 将 left_page和right_page结果以字典的形式返回，为的是可以添加到context中，可以渲染到页面上
        return {
            'left_page':left_page,
            'right_page':right_page,
            'left_has_more':left_has_more,
            'right_has_more':right_has_more,

        }


# 课程列表编辑功能
class editCourseList(View):
    def get(self,request):
        pk=request.GET.get('pk')
        course=PubCourse.objects.get(pk=pk)
        teachers=CourseTeacher.objects.all()
        categories=CorseCategory.objects.all()
        context={
            'course':course,
            'categories':categories,
            'teachers':teachers
        }
        return  render(request,'cms/pub_course.html',context=context)
    def post(self,request):
        form=EditCourseListForm(request.POST)
        if form.is_valid():
            pk=form.cleaned_data.get('pk')
            title = form.cleaned_data.get('title')
            video_url = form.cleaned_data.get('video_url')
            cover_url = form.cleaned_data.get('cover_url')
            price = form.cleaned_data.get('price')
            profile = form.cleaned_data.get('profile')
            category_id = form.cleaned_data.get('category_id')
            category = CorseCategory.objects.get(pk=category_id)
            teacher_id = form.cleaned_data.get('teacher_id')
            teacher = CourseTeacher.objects.get(pk=teacher_id)
            durarion = form.cleaned_data.get('durarion')
            PubCourse.objects.filter(pk=pk).update(title=title, video_url=video_url, cover_url=cover_url, price=price,profile=profile, category=category, teacher=teacher, durarion=durarion)
            return restful.ok()
        else:
            message=form.get_error()
            return restful.params_error(message=message)


# 课程列表删除功能
def deleteCourseList(request):
    # 只能用request.POST
    pk=request.POST.get('pk')
    PubCourse.objects.filter(pk=pk).delete()
    return restful.ok()