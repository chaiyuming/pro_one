from django.urls import path
from . import views
app_name='news'
urlpatterns=[
    path('',views.index,name='index'),
    path('detail/<news_id>/',views.news_detail,name='news_detail'),
    path('search/',views.news_search,name='news_search'),
    path('search_list/',views.search_list,name='search_list'),
    path('news_list/',views.news_list,name='news_list'),
    path('add_comment/',views.add_comment,name='add_comment'),
    # path('search/',views.NewsSreach.as_view(),name='news_search')
]