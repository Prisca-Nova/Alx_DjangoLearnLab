from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Book, Author, CustomUser

@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    """Create default groups and assign permissions after migration."""
    
    if sender.name == 'bookshelf':
        # Get content types
        book_content_type = ContentType.objects.get_for_model(Book)
        author_content_type = ContentType.objects.get_for_model(Author)
        user_content_type = ContentType.objects.get_for_model(CustomUser)
        
        # Get all permissions
        book_permissions = Permission.objects.filter(content_type=book_content_type)
        author_permissions = Permission.objects.filter(content_type=author_content_type)
        
        # Create Groups
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        editors_group, created = Group.objects.get_or_create(name='Editors')
        admins_group, created = Group.objects.get_or_create(name='Admins')
        
        # Assign permissions to Viewers group
        can_view_book = Permission.objects.get(codename='can_view_book', content_type=book_content_type)
        can_view_author = Permission.objects.get(codename='can_view_author', content_type=author_content_type)
        viewers_group.permissions.add(can_view_book, can_view_author)
        
        # Assign permissions to Editors group
        can_create_book = Permission.objects.get(codename='can_create_book', content_type=book_content_type)
        can_edit_book = Permission.objects.get(codename='can_edit_book', content_type=book_content_type)
        can_create_author = Permission.objects.get(codename='can_create_author', content_type=author_content_type)
        can_edit_author = Permission.objects.get(codename='can_edit_author', content_type=author_content_type)
        
        editors_group.permissions.add(
            can_view_book, can_create_book, can_edit_book,
            can_view_author, can_create_author, can_edit_author
        )
        
        # Assign all permissions to Admins group
        admins_group.permissions.add(*book_permissions)
        admins_group.permissions.add(*author_permissions)
        
        print("Groups and permissions created successfully!")