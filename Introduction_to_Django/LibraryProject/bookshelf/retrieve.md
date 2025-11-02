
```markdown
# Retrieve Operation

```python
from bookshelf.models import Book

books = Book.objects.all()
print(list(books))
