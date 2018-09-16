from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.generic import View
from django.views.decorators.http import require_POST,require_GET
from apps.news.models import NewsCategory,News,Banner
# from .models import AddBanner
from utils import restful
from .forms import FormNewsCategory,WriteNewsForm,AddBannerForm,editBannerForm,EditNewslistForm,CorseCategory,CourseTeacher,PubCourse
# 因为在settinds配置了media文件，所以要导入setting
from django.conf import settings
from apps.pro_one_auth.models import User
import os
import qiniu
from datetime import datetime
# 导入登录的装饰器
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# 导入编辑分类的类
from django.core.paginator import Paginator
# 可以对url进行编辑
from urllib import parse
from django.contrib.auth.decorators import permission_required
from apps.pro_one_auth.decorators import xfz_permissoin_required
from django.contrib.auth import logout
# Create your views here.
#给index函数加一层装饰，表示若是is_staff为0，则无权限访问自动跳转到首页中。
@staff_member_required(login_url='/')
def index(request):
    # for x in range(0,30):
    #     title='标题%s'%x
    #     category=CorseCategory.objects.first()
    #     cover_url='https://static-image.xfz.cn/1534831075_407.png-website.news.list'
    #     teacher=CourseTeacher.objects.first()
    #     price='0.00%s'%x
    #     durarion=x
    #     PubCourse.objects.create(title=title,category=category,cover_url=cover_url,teacher=teacher,price=price)
    return render(request,'cms/index.html')
# cms后台管理新闻列表
@method_decorator([xfz_permissoin_required(News)],name='dispatch')
class NewsList(View):
    def get(self,request):
        categories = NewsCategory.objects.all()
        page = int(request.GET.get('p', 1))
        # 查找功能部分代码
        start=request.GET.get('start')
        end=request.GET.get('end')
        title=request.GET.get('title')
        category_id=int(request.GET.get('category',0))
        newses = News.objects.select_related('category', 'author')
        # 过滤选中时间内的新闻
        if start and end and start !='None' and end !='None':
            print('======================')
            print(start)
            # start和end是字符串,需要转换成时间格式
            start_time=datetime.strptime(start,'%Y/%m/%d')
            end_time=datetime.strptime(end,'%Y/%m/%d')
            import datetime as end_datetime
            end_time=end_time+end_datetime.timedelta(hours=23)+end_datetime.timedelta(minutes=59)+end_datetime.timedelta(milliseconds=59000)
            # __range=()表示在一定的时间范围内
            newses=newses.filter(pub_time__range=(start_time,end_time))
        #     过滤标题中函数指定的新闻
        if title and title!='None':
            print('======================')
            print(title)
            # __icontains表示包含哪些内容
            newses=newses.filter(title__icontains=title)
        #       过滤出分类函数指定的新闻
        if category_id !=0 :
            newses=newses.filter(category=category_id)

        # 创建对象
        paginator = Paginator(newses, 2)
        # 某一页的数据
        pag_objects = paginator.page(page)
        # 调用get_data_pagination函数
        data_pagination=self.get_data_pagination(paginator,pag_objects,count_pages=2)
        context = {
            'paginator': paginator,
            'pag_objects': pag_objects,
            'categories': categories,
            'start':start,
            'end':end,
            'title':title,
            'category_id':category_id,
            # 返回某一页的对象值
            'newses': pag_objects.object_list,
            'url_parameter':parse.urlencode({
                'start':start,
                'end':end,
                'title':title,
                'category_id':category_id
            })
        }
        # 将data_pagination更新到context中，既可以去前端代码中去渲染
        context.update(data_pagination)
        return render(request, 'cms/news_list.html',context=context)
    # 重新定义一个函数，对页码数展示和切换功能，count_pages表示当前页前后展示几页，1...23 24 25 26 27...100。
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
# 新闻列表中的编辑按钮
@method_decorator([xfz_permissoin_required(News)],name='dispatch')
class EditNewsView(View):
    # 编辑新闻时,需要拿到新闻的id
    def get(self,request):
        pk=request.GET.get('pk')
        news=News.objects.get(pk=pk)
        categories=NewsCategory.objects.all()
        context={
            'news':news,
            'categories':categories
        }
        return render(request,'cms/write_news.html',context=context)
    def post(self,request):
        form=EditNewslistForm(request.POST)
        if form.is_valid():
            pk=form.cleaned_data.get('pk')
            title=form.cleaned_data.get('title')
            desc=form.cleaned_data.get('desc')
            thumbnail = form.cleaned_data.get('thumbnail')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            category = NewsCategory.objects.get(pk=category_id)
            News.objects.filter(pk=pk).update(title=title,desc=desc,thumbnail=thumbnail,content=content,category=category)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_error())

# 新闻列表中删除按钮
@xfz_permissoin_required(News)
def DeleteNewsbtn(request):
    pk=request.POST.get('pk')
    try:
        News.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        return restful.params_error(message='该新闻不存在')


# @method_decorator是将一些装饰器装饰在类视图上的，然后在里面可以放一些装饰器
# login_url为登录的url
@method_decorator([login_required(login_url='/auth/login/'),xfz_permissoin_required(News)],name='dispatch')
# 表示改视图只有在登录的时候才能访问
class WriteNewsView(View):
    def get(self,request):
        categories=NewsCategory.objects.all()
        return render(request,'cms/write_news.html',
                      context={
                          'categories':categories
                      })
    def post(self,request):
        form=WriteNewsForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data.get('title')
            desc=form.cleaned_data.get('desc')
            thumbnail=form.cleaned_data.get('thumbnail')
            content=form.cleaned_data.get('content')
            category_id=form.cleaned_data.get('category')
            category=NewsCategory.objects.get(pk=category_id)
            author=request.user
            News.objects.create(title=title,desc=desc,thumbnail=thumbnail,content=content,category=category,author=author)
            print(category)
            print(author)
            return restful.ok()
        else:
            return restful.params_error(message=form.get_error())
@xfz_permissoin_required(NewsCategory)
def news_category(request):
    category_id=request.POST.get('category_id')
    news=News.objects.filter(category=category_id)
    categories=NewsCategory.objects.all()
    return render(request,'cms/news_category.html',
                  context={
                      'categories':categories,
                      'news':news
                  })

# @require_POST表示news_category函数只能采用POST请求
# 创建新闻分类函数
@require_POST
@xfz_permissoin_required(NewsCategory)
def add_news_category(request):
    # name
    name=request.POST.get('name')
    exist=NewsCategory.objects.filter(name=name).exists()
    if not exist:
        NewsCategory.objects.create(name=name)
        # restful.ok()一定要加括号
        return restful.ok()
    else:
        return restful.params_error(message='该分类已经存在！')
# 编辑新闻分类
@require_POST
@xfz_permissoin_required(NewsCategory)
def edit_news_category(request):
    form=FormNewsCategory(request.POST)
    if form.is_valid():
        pk=form.cleaned_data.get('pk')
        name=form.cleaned_data.get('name')
        exist=NewsCategory.objects.filter(name=name).exists()
        if not exist:
            NewsCategory.objects.filter(pk=pk).update(name=name)
            return restful.ok()
        else:
            return restful.params_error(message='该分类已经存在')
    else:
        return restful.params_error(message=form.get_error())
# 删除新闻分类
@require_POST
@xfz_permissoin_required(NewsCategory)
def delete_news_category(request):
    # 删除直接获取PK就行
    pk=request.POST.get('pk')
    try:
        NewsCategory.objects.filter(pk=pk).delete()
        return restful.ok()
    except:
        return restful.params_error(message='这个分类不存在')

# 轮播图管理页面实现
@xfz_permissoin_required(Banner)
def banners(request):
    return render(request,'cms/banners.html')
# 添加轮播图内容页面实现
@xfz_permissoin_required(Banner)
def add_banners(request):
    form=AddBannerForm(request.POST)
    if form.is_valid():
        image_url=form.cleaned_data.get('image_url')
        priority=form.cleaned_data.get('priority')
        link_to=form.cleaned_data.get('link_to')
        banner=Banner.objects.create(image_url=image_url,link_to=link_to,priority=priority)
        # 将创建的轮播图返回，返回的是其id，方便后期编辑修改
        return restful.result(data={'banner_id':banner.pk})
        # return restful.result(data={'banner':banner})
    else:
        return restful.params_error(message=form.get_error())
# 删除轮播图
@xfz_permissoin_required(Banner)
def delete_banners(request):
    # 括号中的’banner_id‘是自己随便定义的，在.js会进行赋值
    banner_id=request.POST.get('banner_id')
    Banner.objects.filter(pk=banner_id).delete()
    return restful.ok()
# 编辑轮播图
@xfz_permissoin_required(Banner)
def edit_banners(request):
    form=editBannerForm(request.POST)
    if form.is_valid():
        pk=form.cleaned_data.get('pk')
        image_url=form.cleaned_data.get('image_url')
        link_to=form.cleaned_data.get('link_to')
        priority=form.cleaned_data.get('priority')
        # 找到轮播图的id然后对其进行修改更新
        Banner.objects.filter(pk=pk).update(image_url=image_url,link_to=link_to,priority=priority)
        return restful.ok()
    else:
        return restful.params_error(message=form.get_error())



# 轮播图页面展示
@xfz_permissoin_required(Banner)
def banner_list(request):
    # Banner.objects.all()是获取所有的banner图，获得的是模型对象
    # .value是将模型对象转换成字典
    # list（）是将字段转换成列表。
    banners=list(Banner.objects.all().values())
    # 将从数据库中获取到的所有的banners返回
    return restful.result(data={'banners':banners})


# 文件上传到服务器
@require_POST
#给upfile_file函数加一层装饰，表示若是is_staff为0，则无权限访问自动跳转到首页中。
@staff_member_required(login_url='/')
def upload_file(request):
    # request.FILES获取所有的文件。
    # 参照request.GET.get('username'),这里的upfile相当于username
    file=request.FILES.get('upfile')
    if not file:
        return restful.params_error(message='没有上传任何文件！')
    name=file.name
        # C:/User/media/a.jpg,其中,settings.MEDIA_ROOT代表C:/User/media/，name代表了a.jpg.
    filepath=os.path.join(settings.MEDIA_ROOT,name)
    with open(filepath,'wb') as fp :
        # chunks为django自带的函数，表示自定读取一定的字节，当遍历文件时每次都上传一定的字节，可以做到一点一点读存，比较安全。
        for chunk in file.chunks():
            fp.write(chunk)
            # request.build_absolute_uri可自动获取当前的协议以及域名
            url=request.build_absolute_uri(settings.MEDIA_URL+name)
            # return restful.result(data={'url':settings.MEDIA_URL+name})
            return restful.result(data={'url':url})


# 文件上传到千牛云，千牛云只能使用get方式请求
@require_GET
#给qntoken函数加一层装饰，表示若是is_staff为0，则无权限访问自动跳转到首页中。
@staff_member_required(login_url='/')
def qntoken(request):
    # 到千牛云上难道access_key,secret_key
    access_key='5ixiJHJFv_euNuH47dr2SCN4wWcGOyJA7RDVKEHt'
    secret_key='FMfUTWJwPkyGkJkQMb2fA_Dy1E2OASYETUs6TThC'
    # 构建鉴权对象
    q=qiniu.Auth(access_key,secret_key)
#     要上传的空间
    bucket='cym-1991'
    # 生成上传 Token
    token=q.upload_token(bucket)
    # 将生成的token返回
    return restful.result(data={'token':token})

# 退出

def LogoutView(request):
    logout(request)
    return redirect('/')


