from django.urls import path
from .views import (
    BlogPostListCreateAPIView,
    BlogPostDetailAPIView,
    BlogCategoryListAPIView,
    BlogCommentCreateAPIView
)

urlpatterns = [
    path('posts/', BlogPostListCreateAPIView.as_view(), name='blog-posts'),
    path('posts/<slug:slug>/', BlogPostDetailAPIView.as_view(), name='blog-detail'),
    path('categories/', BlogCategoryListAPIView.as_view(), name='blog-categories'),
    path('posts/<int:post_id>/comment/', BlogCommentCreateAPIView.as_view(), name='add-comment'),
]
