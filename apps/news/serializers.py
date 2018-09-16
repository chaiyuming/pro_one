from rest_framework import serializers
from .models import News,NewsCategory,Comment
from apps.pro_one_auth.serializers import UserSerializers

# 创建category序列化
class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model=NewsCategory
        fields=('id','name')

# djangorestframwork可以更好的将django模型转换为json对象，以方便ajax使用。
# 创建序列化
class NewsSerializers(serializers.ModelSerializer):
    # 当访问category这个字段时，会自动去访问NewsSerializers()这个函数
    category=CategorySerializers()
    author=UserSerializers()
    class Meta:
        model=News
        # 其中‘category’,'author',是通过外键引入的，需要分别再去写一个序列化，告诉以后当需要category字段的时候需要提取哪些字段。
        fields=('id','title','desc','thumbnail','pub_time','category','author')

class CommentSerializers(serializers.ModelSerializer):
    author=UserSerializers()
    class Meta:
        model=Comment
        fields=('id','content','pub_time','author')