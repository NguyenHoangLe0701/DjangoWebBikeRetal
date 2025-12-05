"""
API Rate Limiting Middleware
"""
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
import time

class APIRateLimitMiddleware(MiddlewareMixin):
    """
    Rate limiting middleware cho API endpoints
    """
    
    # Rate limits (requests per time window)
    RATE_LIMITS = {
        '/api/dashboard/': {'requests': 100, 'window': 60},  # 100 requests per minute
        '/api/bikes/': {'requests': 200, 'window': 60},  # 200 requests per minute
        '/api/notifications/': {'requests': 50, 'window': 60},  # 50 requests per minute
        '/api/rentals/': {'requests': 30, 'window': 60},  # 30 requests per minute
    }
    
    # Default rate limit
    DEFAULT_LIMIT = {'requests': 100, 'window': 60}
    
    def process_request(self, request):
        # Only apply to API endpoints
        if not request.path.startswith('/api/'):
            return None
        
        # Skip rate limiting for admin users
        if request.user.is_authenticated and request.user.is_staff:
            return None
        
        # Get client identifier
        client_id = self.get_client_id(request)
        
        # Get rate limit for this endpoint
        rate_limit = self.get_rate_limit(request.path)
        
        # Check rate limit
        cache_key = f'api_rate_limit_{client_id}_{request.path}'
        requests = cache.get(cache_key, 0)
        
        if requests >= rate_limit['requests']:
            return JsonResponse({
                'status': 'error',
                'message': f'Rate limit exceeded. Maximum {rate_limit["requests"]} requests per {rate_limit["window"]} seconds.',
                'retry_after': rate_limit['window']
            }, status=429)
        
        # Increment counter
        cache.set(cache_key, requests + 1, rate_limit['window'])
        
        return None
    
    def get_client_id(self, request):
        """Get unique identifier for client"""
        if request.user.is_authenticated:
            return f'user_{request.user.id}'
        else:
            # Use IP address for anonymous users
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR', 'unknown')
            return f'ip_{ip}'
    
    def get_rate_limit(self, path):
        """Get rate limit configuration for path"""
        for endpoint, limit in self.RATE_LIMITS.items():
            if path.startswith(endpoint):
                return limit
        return self.DEFAULT_LIMIT

