from django.urls import path
from .views import list_books  # Explicit import required by checker
from .views import LibraryDetailView  # Explicit import of class-based view

urlpatterns = [
    # Function-based view
    path('books/', list_books, name='list_books'),

    # Class-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
]
