from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Book, Author

# ============ BOOK VIEWS ============

@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_list(request):
    """View all books - requires can_view_book permission"""
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
def book_detail(request, pk):
    """View book details - requires can_view_book permission"""
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
def book_create(request):
    """Create a new book - requires can_create_book permission"""
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        
        if title and author:
            book = Book.objects.create(
                title=title,
                author=author,
                description=description,
                created_by=request.user
            )
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('book_detail', pk=book.pk)
    
    return render(request, 'bookshelf/book_form.html', {'action': 'Create'})

@login_required
@permission_required('bookshelf.can_edit_book', raise_exception=True)
def book_edit(request, pk):
    """Edit a book - requires can_edit_book permission"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.title = request.POST.get('title', book.title)
        book.author = request.POST.get('author', book.author)
        book.description = request.POST.get('description', book.description)
        book.save()
        
        messages.success(request, f'Book "{book.title}" updated successfully!')
        return redirect('book_detail', pk=book.pk)
    
    return render(request, 'bookshelf/book_form.html', {'book': book, 'action': 'Edit'})

@login_required
@permission_required('bookshelf.can_delete_book', raise_exception=True)
def book_delete(request, pk):
    """Delete a book - requires can_delete_book permission"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

# ============ AUTHOR VIEWS ============

@login_required
@permission_required('bookshelf.can_view_author', raise_exception=True)
def author_list(request):
    """View all authors - requires can_view_author permission"""
    authors = Author.objects.all()
    return render(request, 'bookshelf/author_list.html', {'authors': authors})

@login_required
@permission_required('bookshelf.can_create_author', raise_exception=True)
def author_create(request):
    """Create a new author - requires can_create_author permission"""
    if request.method == 'POST':
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        
        if name:
            author = Author.objects.create(name=name, bio=bio)
            messages.success(request, f'Author "{author.name}" created successfully!')
            return redirect('author_list')
    
    return render(request, 'bookshelf/author_form.html', {'action': 'Create'})

@login_required
@permission_required('bookshelf.can_edit_author', raise_exception=True)
def author_edit(request, pk):
    """Edit an author - requires can_edit_author permission"""
    author = get_object_or_404(Author, pk=pk)
    
    if request.method == 'POST':
        author.name = request.POST.get('name', author.name)
        author.bio = request.POST.get('bio', author.bio)
        author.save()
        
        messages.success(request, f'Author "{author.name}" updated successfully!')
        return redirect('author_list')
    
    return render(request, 'bookshelf/author_form.html', {'author': author, 'action': 'Edit'})

# ============ CLASS-BASED VIEWS ============

class BookListView(PermissionRequiredMixin, ListView):
    """Class-based view for listing books"""
    model = Book
    template_name = 'bookshelf/book_list_cbv.html'
    context_object_name = 'books'
    permission_required = 'bookshelf.can_view_book'
    raise_exception = True

class AuthorDetailView(PermissionRequiredMixin, DetailView):
    """Class-based view for author details"""
    model = Author
    template_name = 'bookshelf/author_detail.html'
    context_object_name = 'author'
    permission_required = 'bookshelf.can_view_author'
    raise_exception = True

# ============ DASHBOARD VIEW ============

@login_required
def dashboard(request):
    """Main dashboard view with permission checks"""
    context = {
        'user': request.user,
        'can_view_book': request.user.has_perm('bookshelf.can_view_book'),
        'can_create_book': request.user.has_perm('bookshelf.can_create_book'),
        'can_edit_book': request.user.has_perm('bookshelf.can_edit_book'),
        'can_delete_book': request.user.has_perm('bookshelf.can_delete_book'),
        'can_view_author': request.user.has_perm('bookshelf.can_view_author'),
        'can_create_author': request.user.has_perm('bookshelf.can_create_author'),
        'can_edit_author': request.user.has_perm('bookshelf.can_edit_author'),
        'can_delete_author': request.user.has_perm('bookshelf.can_delete_author'),
    }
    return render(request, 'bookshelf/dashboard.html', context)