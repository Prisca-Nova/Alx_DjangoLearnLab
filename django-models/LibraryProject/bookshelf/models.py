from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author}"

    class Meta:
        # Add ordering for consistent display
        ordering = ['title']
        # Add verbose names for better admin display
        verbose_name = "Book"
        verbose_name_plural = "Books"