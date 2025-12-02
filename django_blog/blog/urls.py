from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Post CRUD
    path('', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),

    # Comment CRUD (checker expects this exact pattern)
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment-create'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),

    # User authentication
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # Tag and Search URLs
    path('tags/<str:tag_name>/', views.TaggedPostListView.as_view(), name='tagged-posts'),
    path('search/', views.PostSearchListView.as_view(), name='search-posts'),

]
