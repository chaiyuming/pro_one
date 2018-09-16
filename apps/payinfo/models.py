from django.db import models
from shortuuidfield import ShortUUIDField

# Create your models here.
# 创建付费资讯模型
class PayinfoModel(models.Model):
    price=models.FloatField()
    # 文件的路径
    path=models.URLField(max_length=100)
    title=models.CharField(max_length=100)
    profile=models.CharField(max_length=100)

class payinfoOrder(models.Model):
    # 防止paysapi对课程订单id与付费咨询id搞错，这里使用ShortUUIDField来定义一个uid。
    uid=ShortUUIDField(primary_key=True)
    payinfo=models.ForeignKey('PayinfoModel',on_delete=models.DO_NOTHING)
    amount=models.FloatField()
    buyer=models.ForeignKey('pro_one_auth.User',on_delete=models.DO_NOTHING)
    # 支付方式，1代表支付宝，2代表微信,0表示未知
    isstyle=models.SmallIntegerField(default=0)
    # 支付状态，1代表未支付，2代表已支付，SmallIntergerFiled()代表数字类型
    status=models.SmallIntegerField()


