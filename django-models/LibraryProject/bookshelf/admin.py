from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Current configuration (keep what you have)
    list_display = ("title", "author", "publication_year")
    list_filter = ("publication_year",)
    search_fields = ("title", "author")
    
    # Additional enhancements you can add:
    list_per_page = 25  # Control how many items show per page
    ordering = ('title',)  # Default ordering
    
    # If you want to make fields editable directly from list view
    # list_editable = ('publication_year',)
    
    # If you add more fields to your model later, you can use:
    # fieldsets = (
    #     (None, {
    #         'fields': ('title', 'author', 'publication_year')
    #     }),
    # )