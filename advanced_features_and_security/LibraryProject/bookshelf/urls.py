from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard_view, name='dashboard'),
    
    # Book URLs
    path('books/', views.book_list_view, name='book_list'),
    path('books/cbv/', views.BookListView.as_view(), name='book_list_cbv'),
    path('books/<int:pk>/', views.book_detail_view, name='book_detail'),
    path('books/create/', views.book_create_view, name='book_create'),
    path('books/<int:pk>/edit/', views.book_edit_view, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete_view, name='book_delete'),
    
    # Author URLs
    path('authors/', views.author_list_view, name='author_list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('authors/create/', views.author_create_view, name='author_create'),
    path('authors/<int:pk>/edit/', views.author_edit_view, name='author_edit'),
]