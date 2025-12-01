from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.models import ContentType

class CustomUserManager(BaseUserManager):
    """Custom manager for the CustomUser model."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular user with email and password."""
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a superuser with email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    """Custom user model with additional fields."""
    
    # Remove username field, use email instead
    username = None
    email = models.EmailField(_('email address'), unique=True)
    
    # Additional fields as per requirements
    date_of_birth = models.DateField(
        _('date of birth'), 
        null=True, 
        blank=True,
        help_text=_('Enter your date of birth')
    )
    profile_photo = models.ImageField(
        _('profile photo'), 
        upload_to='profile_photos/',
        null=True, 
        blank=True,
        help_text=_('Upload your profile photo')
    )
    
    # Set email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    # Use the custom manager
    objects = CustomUserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        # Add default permissions
        permissions = [
            ("can_view_dashboard", "Can view dashboard"),
            ("can_manage_users", "Can manage users"),
        ]
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}".strip()


class Book(models.Model):
    """Book model with custom permissions."""
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    description = models.TextField()
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    created_by = models.ForeignKey(
        'CustomUser', 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='books_created'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('book')
        verbose_name_plural = _('books')
        # CUSTOM PERMISSIONS AS REQUIRED
        permissions = [
            ("can_view_book", "Can view book details"),
            ("can_create_book", "Can create new book"),
            ("can_edit_book", "Can edit existing book"),
            ("can_delete_book", "Can delete book"),
        ]
    
    def __str__(self):
        return self.title


class Author(models.Model):
    """Author model with custom permissions."""
    name = models.CharField(max_length=100)
    bio = models.TextField()
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    
    class Meta:
        verbose_name = _('author')
        verbose_name_plural = _('authors')
        # CUSTOM PERMISSIONS AS REQUIRED
        permissions = [
            ("can_view_author", "Can view author details"),
            ("can_create_author", "Can create new author"),
            ("can_edit_author", "Can edit existing author"),
            ("can_delete_author", "Can delete author"),
        ]
    
    def __str__(self):
        return self.name