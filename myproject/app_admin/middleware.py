from django.core.cache import cache
from django.http import HttpResponseTooManyRequests
from django.utils import timezone
from datetime import timedelta
import time

class RateLimitMiddleware:
    """
    Middleware để giới hạn số lượng request từ một IP
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Cấu hình rate limit
        self.rate_limit = {
            'login': {'requests': 5, 'window': 300},  # 5 requests per 5 minutes
            'register': {'requests': 3, 'window': 600},  # 3 requests per 10 minutes
            'forgot_password': {'requests': 3, 'window': 3600},  # 3 requests per hour
            'default': {'requests': 100, 'window': 60},  # 100 requests per minute
        }

    def __call__(self, request):
        # Lấy IP của client
        ip_address = self.get_client_ip(request)
        
        # Xác định loại request
        path = request.path
        if '/login/' in path or '/accounts/login/' in path:
            limit_type = 'login'
        elif '/register/' in path or '/accounts/signup/' in path:
            limit_type = 'register'
        elif '/forgot-password/' in path:
            limit_type = 'forgot_password'
        else:
            limit_type = 'default'
        
        # Kiểm tra rate limit
        if not self.check_rate_limit(ip_address, limit_type):
            return HttpResponseTooManyRequests(
                '<h1>429 Too Many Requests</h1>'
                '<p>Bạn đã gửi quá nhiều yêu cầu. Vui lòng thử lại sau vài phút.</p>',
                content_type='text/html'
            )
        
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Lấy IP address của client"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def check_rate_limit(self, ip_address, limit_type):
        """Kiểm tra xem IP có vượt quá rate limit không"""
        config = self.rate_limit.get(limit_type, self.rate_limit['default'])
        key = f'rate_limit:{limit_type}:{ip_address}'
        
        # Lấy số lượng requests hiện tại
        current = cache.get(key, 0)
        
        if current >= config['requests']:
            return False
        
        # Tăng counter
        cache.set(key, current + 1, config['window'])
        return True

