from django.db import models

# Create your models here.
# 教师分类
class teacherCategory(models.Model):
    name=models.CharField(max_length=100)
# 课程讲师
class CourseTeacher(models.Model):
    username=models.CharField(max_length=100)
    # 工作职位
    jobtitle=models.CharField(max_length=100)
    category=models.ForeignKey('teacherCategory',on_delete=models.DO_NOTHING,related_name='teacher')
    profile=models.TextField()
    # 头像
    avatar=models.URLField()

#    课程分类
class CorseCategory(models.Model):
    name=models.CharField(max_length=100)

#发布课程
class PubCourse(models.Model):
    title=models.CharField(max_length=100)
    # 视频链接
    video_url=models.URLField(default='')
    # 封面图的链接
    cover_url=models.URLField()
    # 价格，课程是否需要购买
    price=models.FloatField()
    # 课程的持续时间,代表的是总共有多少秒。
    durarion=models.IntegerField()
    # 课程简介
    profile=models.TextField()
    # 发布时间
    pub_time=models.DateTimeField(auto_now_add=True)
    # models.DO_NOTHING表示什么事情都不做
    category=models.ForeignKey('CorseCategory',on_delete=models.DO_NOTHING,related_name='course')
    teacher=models.ForeignKey('CourseTeacher',on_delete=models.DO_NOTHING)

# 课程订单,真正付费之前先产生一个订单
class CourseOrder(models.Model):
    # 订单产生的时间
    order_time=models.DateTimeField(auto_now_add=True)
    # 金额
    amount=models.FloatField()
    # 支付状态，1代表未支付，2代表已支付，SmallIntergerFiled()代表数字类型
    status=models.SmallIntegerField()
    # 购买的课程
    order_name=models.ForeignKey('PubCourse',on_delete=models.DO_NOTHING)
    # 购买者
    buyer=models.ForeignKey('pro_one_auth.User',on_delete=models.DO_NOTHING)
    # 支付方式，1代表支付宝，2代表微信,0表示未知
    isstyle=models.SmallIntegerField(default=0)

