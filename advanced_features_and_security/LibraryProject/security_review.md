# Security Review

## Implemented Measures

### HTTPS Enforcement
- SECURE_SSL_REDIRECT ensures all traffic uses HTTPS.
- HSTS (SECURE_HSTS_SECONDS, INCLUDE_SUBDOMAINS, PRELOAD) forces browsers to use HTTPS for one year.

### Cookie Security
- SESSION_COOKIE_SECURE and CSRF_COOKIE_SECURE ensure all cookies are sent only via HTTPS.

### Secure Headers
- X_FRAME_OPTIONS = DENY prevents clickjacking.
- SECURE_CONTENT_TYPE_NOSNIFF prevents MIME type sniffing.
- SECURE_BROWSER_XSS_FILTER enables basic XSS protection.

## Improvements (Optional)
- Add CSP (already done).
- Rotate TLS certificates frequently.
- Use HTTPOnly cookies.
