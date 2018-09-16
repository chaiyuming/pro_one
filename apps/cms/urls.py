from django.urls import path
from . import views,course_views,staff_views,add_views

app_name='cms'
urlpatterns=[
    path('',views.index,name='index'),
    path('write_news/',views.WriteNewsView.as_view(),name='write_news'),
    path('news_list/',views.NewsList.as_view(),name='news_list'),
    path('edit_news/',views.EditNewsView.as_view(),name='edit_news'),
    path('delete_news/',views.DeleteNewsbtn,name='delete_news'),
    path('news_category/',views.news_category,name='news_category'),
    path('add_news_category/',views.add_news_category,name='add_news_category'),
    path('edit_news_category/',views.edit_news_category,name='edit_news_category'),
    path('delete_news_category/',views.delete_news_category,name='delete_news_category'),
    path('banners/',views.banners,name='banners'),
    path('add_banners/',views.add_banners,name='add_banners'),
    path('delete_banners/',views.delete_banners,name='delete_banners'),
    path('edit_banners/',views.edit_banners,name='edit_banners'),
    path('banner_list/',views.banner_list,name='banner_list'),
    path('upload_file/',views.upload_file,name='upload_file'),
    path('qntoken/',views.qntoken,name='qntoken'),
    path('logout/',views.LogoutView,name='logout'),
]

# 发布课程url
urlpatterns += [
    path('pub_course/',course_views.PubCourses.as_view(),name='pub_course'),
    path('course_category/',course_views.course_category,name='course_category'),
    path('add_course_category/',course_views.add_course_category,name='add_course_category'),
    path('edit_course_category/',course_views.edit_course_category,name='edit_course_category'),
    path('delete_course_category/',course_views.delete_course_category,name='delete_course_category'),
    path('course_list/',add_views.CourseList.as_view(),name='course_list'),
    path('course_edit/',add_views.editCourseList.as_view(),name='course_edit'),
    path('course_delete/',add_views.deleteCourseList,name='course_delete'),
]
# 教师信息
urlpatterns +=[
    path('teacher/',course_views.TeacherView.as_view(),name='teacher'),
    # path('teacher_token/',course_views.teacher_token,name='token'),
    path('teacher_category/',course_views.teacher_category,name='teacher_category'),
    path('add_teacher_category/',course_views.add_teacher_category,name='add_teacher_category'),
    path('edit_teacher_category/',course_views.edit_teacher_category,name='edit_teacher_category'),
    path('delete_teacher_group/',course_views.delete_teacher_group,name='delete_teacher_group'),
    path('teacher_list/',course_views.TeacherList.as_view(),name='teacher_list'),
    path('edit_teacher_list/',course_views.TeacherListEdit.as_view(),name='edit_teacher_list'),
    path('delete_teacher_list/',course_views.delete_teacher_list,name='delete_teacher_list'),
]
# 管理员工url
urlpatterns +=[
    path('staff/',staff_views.staff,name='staff'),
    path('add_staff/',staff_views.AddStaff.as_view(),name='add_staff'),
    path('delete_staff/',staff_views.DeleteStaff,name='delete_staff'),
]