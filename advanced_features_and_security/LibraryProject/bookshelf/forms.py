# bookshelf/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re
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

# ============ SECURITY TASK: ADD ExampleForm ============

class ExampleForm(forms.Form):
    """
    Secure form example that demonstrates proper input validation
    and sanitation to prevent various attacks.
    This form is required for the security task implementation.
    """
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Your Name",
        help_text="Enter your name (letters, spaces, hyphens, apostrophes, and periods only)"
    )
    
    email = forms.EmailField(
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        label="Email Address"
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=True,
        label="Message",
        help_text="Enter your message (HTML tags will be removed for security)"
    )
    
    def clean_name(self):
        """Sanitize and validate name field to prevent XSS attacks"""
        name = self.cleaned_data.get('name')
        
        if not name:
            return name
            
        # Remove any HTML tags to prevent XSS
        name = re.sub(r'<[^>]*>', '', name)
        
        # Validate name contains only letters, spaces, and common punctuation
        if not re.match(r'^[A-Za-z\s\-\'\.]+$', name):
            raise ValidationError('Name contains invalid characters. Only letters, spaces, hyphens, apostrophes, and periods are allowed.')
        
        return name.strip()
    
    def clean_message(self):
        """Sanitize message content to prevent XSS attacks"""
        message = self.cleaned_data.get('message')
        
        if not message:
            return message
            
        # Remove script tags and other potentially dangerous HTML
        message = re.sub(r'<script[^>]*>.*?</script>', '', message, flags=re.DOTALL | re.IGNORECASE)
        message = re.sub(r'<[^>]*>', '', message)  # Remove all remaining HTML tags
        
        # Additional security: escape special characters
        message = message.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        return message.strip()