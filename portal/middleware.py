"""
Custom middleware for additional security headers and protections.
"""
from django.conf import settings


class SecurityHeadersMiddleware:
    """
    Middleware to add comprehensive security headers to all responses.
    
    Headers added:
    - Content-Security-Policy (CSP)
    - Referrer-Policy
    - Permissions-Policy
    - X-Content-Type-Options
    - X-Frame-Options
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Content Security Policy
        csp_directives = []
        if hasattr(settings, 'CSP_DEFAULT_SRC'):
            csp_directives.append(f"default-src {' '.join(settings.CSP_DEFAULT_SRC)}")
        if hasattr(settings, 'CSP_SCRIPT_SRC'):
            csp_directives.append(f"script-src {' '.join(settings.CSP_SCRIPT_SRC)}")
        if hasattr(settings, 'CSP_STYLE_SRC'):
            csp_directives.append(f"style-src {' '.join(settings.CSP_STYLE_SRC)}")
        if hasattr(settings, 'CSP_FONT_SRC'):
            csp_directives.append(f"font-src {' '.join(settings.CSP_FONT_SRC)}")
        if hasattr(settings, 'CSP_IMG_SRC'):
            csp_directives.append(f"img-src {' '.join(settings.CSP_IMG_SRC)}")
        if hasattr(settings, 'CSP_CONNECT_SRC'):
            csp_directives.append(f"connect-src {' '.join(settings.CSP_CONNECT_SRC)}")
        if hasattr(settings, 'CSP_FRAME_ANCESTORS'):
            csp_directives.append(f"frame-ancestors {' '.join(settings.CSP_FRAME_ANCESTORS)}")
        if hasattr(settings, 'CSP_BASE_URI'):
            csp_directives.append(f"base-uri {' '.join(settings.CSP_BASE_URI)}")
        if hasattr(settings, 'CSP_FORM_ACTION'):
            csp_directives.append(f"form-action {' '.join(settings.CSP_FORM_ACTION)}")
        
        if csp_directives:
            response['Content-Security-Policy'] = '; '.join(csp_directives)
        
        # Referrer Policy
        if hasattr(settings, 'SECURE_REFERRER_POLICY'):
            response['Referrer-Policy'] = settings.SECURE_REFERRER_POLICY
        
        # Permissions Policy (formerly Feature-Policy)
        # Restrict access to sensitive browser features
        permissions_policy = [
            'geolocation=()',
            'microphone=()',
            'camera=()',
            'payment=()',
            'usb=()',
            'magnetometer=()',
            'gyroscope=()',
            'accelerometer=()',
        ]
        response['Permissions-Policy'] = ', '.join(permissions_policy)
        
        # X-Content-Type-Options (prevent MIME sniffing)
        response['X-Content-Type-Options'] = 'nosniff'
        
        # X-Frame-Options (clickjacking protection)
        response['X-Frame-Options'] = 'DENY'
        
        # Cross-Origin-Opener-Policy
        if hasattr(settings, 'SECURE_CROSS_ORIGIN_OPENER_POLICY'):
            response['Cross-Origin-Opener-Policy'] = settings.SECURE_CROSS_ORIGIN_OPENER_POLICY
        
        # Cross-Origin-Resource-Policy
        response['Cross-Origin-Resource-Policy'] = 'same-origin'
        
        return response
