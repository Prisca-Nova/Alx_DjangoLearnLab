import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from bookshelf.models import Book

# CREATE
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print("Created:", book)

# RETRIEVE
books = Book.objects.all()
print("All books:", list(books))

# UPDATE
book.title = "Nineteen Eighty-Four"
book.save()
books = Book.objects.all()
print("After update:", list(books))

# DELETE
book.delete()
books = Book.objects.all()
print("After delete:", list(books))
