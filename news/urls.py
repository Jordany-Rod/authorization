from django.urls import path

from .views import (PostList, PostDetail, PostCreateNews, PostCreateArticles,
                    PostUpdateNews, PostUpdateArticles, PostDeleteNews, PostDeleteArticles )


urlpatterns = [
   path('', PostList.as_view(), name='post_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('news/create/', PostCreateNews.as_view(), name='post_create_news'),
   path('news/<int:pk>/edit/', PostUpdateNews.as_view(), name='post_update_news'),
   path('news/<int:pk>/delete', PostDeleteNews.as_view(), name='post_delete_news'),
   path('articles/create/', PostCreateArticles.as_view(), name='post_create_articles'),
   path('articles/<int:pk>/edit/', PostUpdateArticles.as_view(), name='post_update_articles'),
   path('articles/<int:pk>/delete', PostDeleteArticles.as_view(), name='post_delete_articles'),
]