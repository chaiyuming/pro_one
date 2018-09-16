from django.urls import path
from . import views
# 应用命名空间
app_name='course'
urlpatterns=[
    path('',views.course_index,name='course_index'),
    path('detail/<course_id>/',views.course_detail,name='course_detail'),
    path('course_token/',views.course_token,name='course_token'),
    path('course_order/',views.course_order,name='course_order'),
    path('notify_url/',views.notify_url,name='notify_url'),
    path('order_key/',views.order_key,name='order_key'),
]