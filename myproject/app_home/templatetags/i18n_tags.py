from django import template
from django.utils.translation import get_language, activate, gettext_lazy as _

register = template.Library()

@register.simple_tag
def get_current_language():
    """Lấy ngôn ngữ hiện tại"""
    return get_language()

@register.simple_tag
def get_available_languages():
    """Lấy danh sách ngôn ngữ có sẵn"""
    from django.conf import settings
    return getattr(settings, 'LANGUAGES', [('vi', 'Tiếng Việt')])

