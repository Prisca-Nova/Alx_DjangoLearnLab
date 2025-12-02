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
    # ... other apps ...
    'csp',  # For Content Security Policy
]

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
