# ==================== SECURITY SETTINGS ====================

# Debug settings - MUST be False for security
DEBUG = False

# Security middleware settings
SECURE_BROWSER_XSS_FILTER = True  # Enables browser's XSS filtering
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevents MIME type sniffing
X_FRAME_OPTIONS = 'DENY'  # Prevents clickjacking by denying framing

# Cookie security - Only send cookies over HTTPS
CSRF_COOKIE_SECURE = True  # CSRF cookies only over HTTPS
SESSION_COOKIE_SECURE = True  # Session cookies only over HTTPS

# If you're using django-csp (optional but recommended for CSP)
# Add 'csp' to INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bookshelf',
    'csp',  # For Content Security Policy
]
AUTH_USER_MODEL = 'bookshelf.CustomUser'

# Add CSP middleware
MIDDLEWARE = [
    # ... other middleware ...
    'csp.middleware.CSPMiddleware',
]

# Content Security Policy settings
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")
CSP_SCRIPT_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'", "data:")

# ==================== HTTPS & SECURITY ENFORCEMENT ====================

# Redirect all HTTP requests to HTTPS
SECURE_SSL_REDIRECT = True

# HTTP Strict Transport Security
SECURE_HSTS_SECONDS = 31536000          # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Secure cookies (already done but included for clarity)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Secure headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
