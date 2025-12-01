from django.apps import AppConfig

class BookshelfConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookshelf'
    
    def ready(self):
        """Import signals when the app is ready."""
        import bookshelf.signals