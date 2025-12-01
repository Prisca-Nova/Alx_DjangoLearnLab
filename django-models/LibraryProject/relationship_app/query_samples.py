from .models import Author, Book, Library

# 1. All books by a specific author
def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return list(Book.objects.filter(author=author))

# 2. List all books in a library
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return list(library.books.all())

# 3. Retrieve the librarian for a library
def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.librarian
