from django.shortcuts import render
from .models import News, NewsCategory, Comment, Banner
from django.conf import settings
from django.views.decorators.http import require_GET, require_POST
from utils import restful
from .serializers import NewsSerializers, CommentSerializers
from django.http import Http404
from .forms import AddCommentForm
# filter() 等方法中的关键字参数查询都是一起进行“AND” 的。 如果你需要执行更复杂的查询（例如OR 语句），你可以使用Q 对象。
from django.db.models import Q
from django.views.generic import View
# login_required:只能针对传统的页面跳转（如果没有登入就跳转到login_url指定的页面，但是他不能处理这种Ajax请求
# 就是说如果通过ajax请求去访问一个需要授权的页面，那么这个装饰器的页面跳转就能就失效了,那么就需要我们自己定义一个装饰器）
from django.contrib.auth.decorators import login_required
from apps.pro_one_auth.decorators import xfz_login_required

# Create your views here.
# 首页新闻展示代码
def index(request):
    # .select_related()表示在查询新闻的时候一起查询与新闻相关的某些内容，只能是通过外键传入的。
    # 在视图函数中将新闻的内容和分类先查询出来
    newes = News.objects.select_related('category', 'author')[0:settings.ONE_PAGE__NEWS_COUNT]
    categories = NewsCategory.objects.all()
    banner = Banner.objects.all()
    return render(request, 'news/index.html', context={
        'newes': newes,
        'categories': categories,
        'banners': banner
    })


# 加载更多按钮代码
# 新闻列表只能用get方式请求
# 首页中的新闻列表
@require_GET
def news_list(request):
    # 1是默认参数，表示当没有传入p时，就会自动传入这个默认参数
    # 通过前端获取来的值为字符串，通过int将其转化为整型
    page = int(request.GET.get('p', 1))
    category_id = int(request.GET.get('category_id', 0))
    start = settings.ONE_PAGE__NEWS_COUNT * (page - 1)
    end = start + settings.ONE_PAGE__NEWS_COUNT
    # 通关News.objects.all()获得的是模型对象，但是新闻列表的加载是通过ajax方式，而ajax是通过json数据进行交互的
    # .values()可以将Queryset中的模型对象（比如：News（）对象）转化为字典
    # [start:end]是切片的形式
    # 通过list（）将字典转化为列表，序列化,这样就得到了key值。
    # newses=list(News.objects.all()[start:end].values())
    if category_id == 0:
        newses = News.objects.all()[start:end]
    else:
        newses = News.objects.filter(category_id=category_id)[start:end]
    # many=True表示序列化很多数据，而不是单条数据
    # 将获取到的newsesQueryset对象传入NewSerializers()函数中，进行序列化
    serializer = NewsSerializers(newses, many=True)
    # 通过restful.result(data=newses)方式返回
    # return restful.result(data=newses)
    return restful.result(data=serializer.data)


# 如果在url定义了参数，那么在视图函数中也要定义相应的函数
def news_detail(request, news_id):
    # 捕获异常，当输入的新闻id错误时，就报404错误！
    try:
        newses = News.objects.select_related('category', 'author').get(pk=news_id)
        content = {
            'newses': newses
        }
        return render(request, 'news/news_detail.html',
                      context=content)
    # 如果错误的类型为DoesNotExist,抛出Http404错误。
    except News.DoesNotExist:
        raise Http404


@require_POST
@xfz_login_required
def add_comment(request):
    form = AddCommentForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data.get('content')
        news_id = form.cleaned_data.get('news_id')
        news = News.objects.get(pk=news_id)
        comment = Comment.objects.create(content=content, news=news, author=request.user)
        #         通过ajax将数据上传到服务器，需要传递的时json对象。而CommentNews是模型对象，需要现将其进行序列化。
        #         这里不用添加many=True,因为.create获取的值不是Queryset对象。
        serializer = CommentSerializers(comment)
        # for i in news.comments.all():
        #     print(i.content)
        # print(content)
        return restful.result(data=serializer.data)
    else:
        return restful.params_error(message=form.get_error())


def news_search(request):
    # q在前端中已经定义
    q = request.GET.get('q')
    name=NewsCategory.objects.get(name='金融科技')
    news2 = News.objects.filter(category=name)
    # news2 = News.objects.all()
    if q and q !='None':
        news = News.objects.filter(Q(title__icontains=q) | Q(content__contains=q) | Q(category__name__contains=q))
        context = {
            'news': news,
            'news2': news2
        }
    else:
        context = {
            'news2': news2
        }
    return render(request, 'news/search.html', context=context)
# class NewsSreach(View):
#     def get(self,request):
#         # q在前端中已经定义
#         q = request.GET.get('q')
#         news2 = News.objects.all()
#         if q:
#             news = News.objects.filter(Q(title__icontains=q) | Q(content__contains=q) | Q(category__name__contains=q))
#             print('*' * 30)
#             print(news.values())
#             print('*' * 30)
#             context = {
#                 'news': news,
#                 'news2': news2
#             }
#         else:
#             context = {
#                 'news2': news2
#             }
#         return render(request, 'news/search.html', context=context)
#     def search(self,q):
#         news = News.objects.filter(Q(title__icontains=q) | Q(content__contains=q) | Q(category__name__contains=q))
#         serializer=NewsSerializers(news,many=True)
#         return restful.result(data=serializer.data)



