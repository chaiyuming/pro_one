from django import forms
from apps.forms import FormMixin

class AddCommentForm(forms.Form,FormMixin):
    # 在form表单中.CharField与.TextField的区别在于，在表单渲染成模板的时候，
    # CharField渲染成Input标签
    # TextField渲染成Textarea标签
    content=forms.CharField(error_messages={
        'required':'请输入评论'
    })
    news_id=forms.IntegerField()
