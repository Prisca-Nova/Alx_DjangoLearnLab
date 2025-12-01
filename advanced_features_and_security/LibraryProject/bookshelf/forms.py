from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """A form for creating new users with all required fields."""
    
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'date_of_birth')
        field_classes = {}

class CustomUserChangeForm(UserChangeForm):
    """A form for updating users with all required fields."""
    
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'date_of_birth', 'profile_photo', 'is_active', 'is_staff', 'is_superuser')