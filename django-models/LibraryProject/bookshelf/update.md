```markdown
# Update Operation

```python
from bookshelf.models import Book

book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

books = Book.objects.all()
print(list(books))
