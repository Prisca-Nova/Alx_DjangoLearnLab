from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

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
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}".strip()