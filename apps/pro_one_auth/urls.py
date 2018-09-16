from django.urls import path
from . import views,forgetViews

app_name='pro_one_auth'
urlpatterns=[
    path('login/',views.LoginView.as_view(),name='LoginView'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('logout/',views.LogoutView,name='logout'),
    path('img_captcha/',views.img_captcha,name='img_captcha'),
    path('sms_captcha/',views.sms_captcha,name='sms_captcha'),
]

urlpatterns +=[
    path('forget_password/',forgetViews.forgetPassword.as_view(),name='forget_password'),
    path('rest_pwd/',forgetViews.rest_pwd,name='rest_pwd'),
    path('modifypassword/',forgetViews.ModifyPassword.as_view(),name='modifypassword'),
]