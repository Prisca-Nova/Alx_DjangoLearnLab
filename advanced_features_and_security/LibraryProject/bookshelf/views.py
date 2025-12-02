# bookshelf/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from .models import Book, Author
from .forms import ExampleForm  # Import ExampleForm

# ============ SECURITY TASK: ADD ExampleForm VIEW ============

@login_required
@csrf_protect
def form_example_view(request):
    """
    Example view demonstrating secure form handling with CSRF protection
    and input validation.
    This view is required for the security task implementation.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            # This data has been validated and sanitized
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Log or process the secure data (example only)
            print(f"Secure form submission: {name}, {email}, {message[:50]}...")
            
            messages.success(request, 'Form submitted securely! Your input has been validated and sanitized.')
            return render(request, 'bookshelf/form_example.html', {
                'form': ExampleForm(),
                'success': True,
                'name': name
            })
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})

# ============ SECURE BOOK VIEWS ============

@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
@csrf_protect
def book_list(request):
    """
    View all books - requires can_view_book permission
    SECURE VERSION: Added safe search functionality and CSRF protection
    """
    search_query = request.GET.get('q', '').strip()
    
    # SECURE: Using Django ORM with safe query construction
    if search_query:
        # Using Q objects for safe, parameterized queries (prevents SQL injection)
        books = Book.objects.filter(
            Q(title__icontains=search_query) | 
            Q(author__name__icontains=search_query)  # Assuming author is a ForeignKey
        ).select_related('author')  # Optimize queries
    else:
        books = Book.objects.all().select_related('author')
    
    # SECURE: Always escape output in template, but also escape here for safety
    safe_search_query = search_query.replace('<', '&lt;').replace('>', '&gt;')
    
    context = {
        'books': books,
        'search_query': safe_search_query,
        'original_search': search_query,  # For forms if needed
    }
    return render(request, 'bookshelf/book_list.html', context)

@login_required
@permission_required('bookshelf.can_view_book', raise_exception=True)
@csrf_protect
def book_detail(request, pk):
    """View book details - requires can_view_book permission"""
    # SECURE: Using get_object_or_404 with proper parameterization
    book = get_object_or_404(Book.objects.select_related('author'), pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

@login_required
@permission_required('bookshelf.can_create_book', raise_exception=True)
@csrf_protect
def book_create(request):
    """Create a new book - requires can_create_book permission"""
    # SECURE: This view should ideally use Django Forms for better security
    # For now, we'll sanitize inputs manually
    
    if request.method == 'POST':
        # SECURE: Get and sanitize inputs
        title = request.POST.get('title', '').strip()
        author_id = request.POST.get('author_id', '').strip()  # Assuming author is selected by ID
        description = request.POST.get('description', '').strip()
        
        # Basic XSS prevention
        title = title.replace('<', '&lt;').replace('>', '&gt;')
        description = description.replace('<', '&lt;').replace('>', '&gt;')
        
        # SECURE: Validate inputs
        if not title:
            messages.error(request, 'Title is required.')
            return render(request, 'bookshelf/book_form.html', {'action': 'Create'})
        
        if not author_id:
            messages.error(request, 'Author is required.')
            return render(request, 'bookshelf/book_form.html', {'action': 'Create'})
        
        try:
            # SECURE: Get author by ID (safe from SQL injection)
            author = Author.objects.get(pk=author_id)
        except (Author.DoesNotExist, ValueError):
            messages.error(request, 'Invalid author selected.')
            return render(request, 'bookshelf/book_form.html', {'action': 'Create'})
        
        # SECURE: Create book with validated data
        book = Book.objects.create(
            title=title,
            author=author,
            description=description,
            created_by=request.user
        )
        messages.success(request, f'Book "{book.title}" created successfully!')
        return redirect('book_detail', pk=book.pk)
    
    # GET request - show form
    authors = Author.objects.all()  # SECURE: Safe query
    return render(request, 'bookshelf/book_form.html', {
        'action': 'Create',
        'authors': authors  # Pass authors for selection
    })

@login_required
@permission_required('bookshelf.can_edit_book', raise_exception=True)
@csrf_protect
def book_edit(request, pk):
    """Edit a book - requires can_edit_book permission"""
    # SECURE: Get book with parameterized query
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        # SECURE: Sanitize inputs
        title = request.POST.get('title', book.title).strip()
        author_id = request.POST.get('author_id', '').strip()
        description = request.POST.get('description', book.description).strip()
        
        # Basic XSS prevention
        title = title.replace('<', '&lt;').replace('>', '&gt;')
        description = description.replace('<', '&lt;').replace('>', '&gt;')
        
        book.title = title
        book.description = description
        
        # Update author if provided
        if author_id:
            try:
                author = Author.objects.get(pk=author_id)
                book.author = author
            except (Author.DoesNotExist, ValueError):
                messages.error(request, 'Invalid author selected.')
        
        book.save()
        
        messages.success(request, f'Book "{book.title}" updated successfully!')
        return redirect('book_detail', pk=book.pk)
    
    # GET request - show form
    authors = Author.objects.all()  # SECURE: Safe query
    return render(request, 'bookshelf/book_form.html', {
        'book': book, 
        'action': 'Edit',
        'authors': authors
    })

@login_required
@permission_required('bookshelf.can_delete_book', raise_exception=True)
@csrf_protect
def book_delete(request, pk):
    """Delete a book - requires can_delete_book permission"""
    # SECURE: Parameterized query
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f'Book "{title}" deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})

# ============ SECURE AUTHOR VIEWS ============

@login_required
@permission_required('bookshelf.can_view_author', raise_exception=True)
@csrf_protect
def author_list(request):
    """View all authors - requires can_view_author permission"""
    # SECURE: Added safe search
    search_query = request.GET.get('q', '').strip()
    
    if search_query:
        # SECURE: Safe query using Q objects
        authors = Author.objects.filter(name__icontains=search_query)
    else:
        authors = Author.objects.all()
    
    # SECURE: Escape search query for display
    safe_search_query = search_query.replace('<', '&lt;').replace('>', '&gt;')
    
    return render(request, 'bookshelf/author_list.html', {
        'authors': authors,
        'search_query': safe_search_query
    })

@login_required
@permission_required('bookshelf.can_create_author', raise_exception=True)
@csrf_protect
def author_create(request):
    """Create a new author - requires can_create_author permission"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        bio = request.POST.get('bio', '').strip()
        
        # SECURE: Sanitize inputs
        name = name.replace('<', '&lt;').replace('>', '&gt;')
        bio = bio.replace('<', '&lt;').replace('>', '&gt;')
        
        if name:
            # SECURE: Check for duplicate names (safe query)
            if Author.objects.filter(name__iexact=name).exists():
                messages.error(request, f'An author named "{name}" already exists.')
            else:
                author = Author.objects.create(name=name, bio=bio)
                messages.success(request, f'Author "{author.name}" created successfully!')
                return redirect('author_list')
        else:
            messages.error(request, 'Author name is required.')
    
    return render(request, 'bookshelf/author_form.html', {'action': 'Create'})

@login_required
@permission_required('bookshelf.can_edit_author', raise_exception=True)
@csrf_protect
def author_edit(request, pk):
    """Edit an author - requires can_edit_author permission"""
    # SECURE: Parameterized query
    author = get_object_or_404(Author, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name', author.name).strip()
        bio = request.POST.get('bio', author.bio).strip()
        
        # SECURE: Sanitize inputs
        name = name.replace('<', '&lt;').replace('>', '&gt;')
        bio = bio.replace('<', '&lt;').replace('>', '&gt;')
        
        # SECURE: Check for duplicate names (excluding current author)
        if name != author.name and Author.objects.filter(name__iexact=name).exists():
            messages.error(request, f'An author named "{name}" already exists.')
        else:
            author.name = name
            author.bio = bio
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
    
    # SECURE: Add safe search functionality
    def get_queryset(self):
        queryset = super().get_queryset().select_related('author')
        search_query = self.request.GET.get('q', '').strip()
        
        if search_query:
            # SECURE: Safe query using Q objects
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(author__name__icontains=search_query)
            )
        
        return queryset
    
    # SECURE: Pass sanitized search query to template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('q', '').strip()
        context['search_query'] = search_query.replace('<', '&lt;').replace('>', '&gt;')
        return context

class AuthorDetailView(PermissionRequiredMixin, DetailView):
    """Class-based view for author details"""
    model = Author
    template_name = 'bookshelf/author_detail.html'
    context_object_name = 'author'
    permission_required = 'bookshelf.can_view_author'
    raise_exception = True

# ============ DASHBOARD VIEW ============

@login_required
@csrf_protect
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