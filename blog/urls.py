from . import views
from django.urls import path
from .views import (
        PostDeleteView,
        UserPostListView,
        CatPostListView, 
        NewPostView,
    )

urlpatterns = [
    path('', views.index, name="Blog-Home"),
    path('post/<str:username>/user/', UserPostListView.as_view(), name="Blog-User"),
    path('post/<str:category>/category/', CatPostListView.as_view(), name="Blog-Cat"),
    path('post/<int:pk>/details/', views.PostDetail, name="Blog-details"),
    path('post/<int:pk>/update/', views.UpdatePost, name="Blog-Update"),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name="Blog-Delete"),
    # path('post/new/', views.newPost, name="Blog-create"),
    path('post/new/', NewPostView.as_view(), name="Blog-create"),

    path('post/about/', views.about, name="Blog-About"),
] 