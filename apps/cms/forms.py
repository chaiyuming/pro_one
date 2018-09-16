from django import forms
from apps.forms import FormMixin
from apps.news.models import News,Banner
from apps.course.models import PubCourse,CourseTeacher,CorseCategory


# 新闻编辑功能表单验证
class FormNewsCategory(forms.Form,FormMixin):
    pk=forms.IntegerField(error_messages={
        'required':'必须传入分类ID'
    })
    name=forms.CharField(max_length=100,min_length=1,error_messages={
        'required':'必须输入分类名称',
        'max_length':'名称最大长度不能超过100',
        'min_length':'名称必须大于等于1',
    })

# 新添新闻部分表单验证
# forms.Model.Form表示直接可以指定该表单是为哪个模型服务的
class WriteNewsForm(forms.ModelForm,FormMixin):
    # 因为.model中的category是外键引入的，这里需要重新定义验证
    category=forms.IntegerField()
    class Meta:
        # 指定服务的模型
        model=News
        # 指定哪些字段需要验证，fields是元祖的形式
        fields=('title','desc','content','thumbnail')
        error_messages={
            'category':{
                'required': '必须输入分类ID'
            },
            'title':{
                'required':'必须输入新闻标题'
            }
        }

# 新闻列表编辑按钮表单验证
# 在添加新闻验证表单的基础上,添加一个新闻id即可
class EditNewslistForm(WriteNewsForm):
    pk=forms.IntegerField()
# 添加轮播图表单验证
class AddBannerForm(forms.ModelForm,FormMixin):
    class Meta:
        model=Banner
        fields=('image_url','priority','link_to')

# 编辑轮播图表单验证
class editBannerForm(forms.ModelForm,FormMixin):
    pk=forms.IntegerField()
    class Meta:
        model=Banner
        fields=('image_url','priority','link_to','pk')


# 添加课程表单验证
class addCourseForm(forms.ModelForm,FormMixin):
    category_id=forms.IntegerField(error_messages={
        'required':'必须输入分类的ID'
    })
    teacher_id=forms.IntegerField(error_messages={
        'required':'必须输入老师的ID'
    })
    class Meta:
        model=PubCourse
        # 排除这几个变量用exclude,我们传递的是category的id，以及teacher的id，所以不需要传递'category','teacher'的模型
        exclude=('pub_time','category','teacher')
        error_messages={
            'video_url':{
                'required':'视频链接不能为空'
            },
            'cover_url':{
                'required':'封面图的链接不能为空'
            },
            'profile':{
                'required':'课程简介不能为空'
            },
            'title':{
                'required':'标题不能为空'
            },
            'price':{
                'required':'价格不能为空'
            }
        }

#课程列表中的编辑功能表单验证
class EditCourseListForm(addCourseForm):
    pk=forms.IntegerField()
# 课程分类验证表单
class CourseCategoryForm(forms.Form,FormMixin):
    pk=forms.IntegerField(error_messages={
        'required':'必须输入分类ID'
    })
    name=forms.CharField(error_messages={
        'required':'必须输入分类名称',
        'max_length':'最大长度不能大于100',
        'min_length':'最小长度不能小于1'
    })

# 添加教师信息信息验证
class TeacherForm(forms.ModelForm,FormMixin):
    category=forms.IntegerField()
    class Meta:
        model=CourseTeacher
        fields=('username','jobtitle','profile','avatar')
        error_messages={
            'username':{
                'required':'请输入教师名字！'
            },
            'jobtitle':{
                'required':'请输入教师的职称'
            },
            'profile':{
                'required':'请输入教师的简介'
            },
            'avatar':{
                'required':'请上传教师的照片'
            },
            'category':'必须输入教师分组'
        }
# 教师列表中编辑按钮
class TeacherListEditForm(TeacherForm):
    pk=forms.IntegerField()
# 教师分组中编辑按钮验证信息
class TeacherCategoryForm(forms.Form,FormMixin):
    pk=forms.IntegerField()
    name=forms.CharField(error_messages={
        'required':'必须输入教师分组',
        'max_length': '最大长度不能大于100',
        'min_length': '最小长度不能小于1'
    })

