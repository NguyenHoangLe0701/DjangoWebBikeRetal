"""
Context processors for templates
"""
from django.conf import settings

def analytics(request):
    """Add analytics settings to template context"""
    return {
        'GOOGLE_ANALYTICS_ID': getattr(settings, 'GOOGLE_ANALYTICS_ID', ''),
        'GOOGLE_ANALYTICS_ENABLED': getattr(settings, 'GOOGLE_ANALYTICS_ENABLED', False),
    }

