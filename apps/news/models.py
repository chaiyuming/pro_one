from django.db import models

# Create your models here.
# 新闻分类表
class NewsCategory(models.Model):
    name=models.CharField(max_length=100)


# 首页新闻部分表
class News(models.Model):
    title=models.CharField(max_length=200)
    desc=models.CharField(max_length=200)
    thumbnail=models.URLField()
    content=models.TextField()
    pub_time=models.DateTimeField(auto_now_add=True)
    # category/author需要引用外键，on_delete=models.SET_NULL当分类被删除后，为空值
    category=models.ForeignKey('NewsCategory',on_delete=models.SET_NULL,null=True,related_name='news')
    author=models.ForeignKey('pro_one_auth.User',on_delete=models.SET_NULL,null=True)

    class Meta:
        # 使用ordering可以指定字段进行排序，以后News.objects提取数据时,就会自动按照指定的字段进行排序
        # －号表示从最近的时间进行排序
        ordering=['-pub_time']

# 新闻评论
class Comment(models.Model):
    content=models.TextField()
    pub_time=models.DateTimeField(auto_now_add=True)
    # 给这个外键定义一个名字，方便一对多的时候直接查询（news.comments.all()）
    news=models.ForeignKey('News',on_delete=models.CASCADE,related_name='comments')
    author=models.ForeignKey('pro_one_auth.User',on_delete=models.CASCADE)

# 添加轮播图
class Banner(models.Model):
    image_url = models.URLField()
    priority = models.IntegerField(default=0)
    link_to = models.URLField()
    pub_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority']