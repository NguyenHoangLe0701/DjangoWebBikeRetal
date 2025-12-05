"""
JWT Authentication for Mobile API
"""
try:
    import jwt
except ImportError:
    jwt = None

from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import get_user_model

try:
    from rest_framework.authentication import BaseAuthentication
    from rest_framework.exceptions import AuthenticationFailed
    from rest_framework.permissions import BasePermission
except ImportError:
    # REST Framework not installed
    BaseAuthentication = object
    AuthenticationFailed = Exception
    BasePermission = object

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    """
    JWT Authentication class for mobile API
    """
    
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return None
        
        token = auth_header.split(' ')[1]
        
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=['HS256']
            )
            user_id = payload.get('user_id')
            
            if not user_id:
                raise AuthenticationFailed('Invalid token')
            
            user = User.objects.get(id=user_id)
            
            if not user.is_active:
                raise AuthenticationFailed('User is inactive')
            
            return (user, token)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token has expired')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token')
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')
    
    def authenticate_header(self, request):
        return 'Bearer'


def generate_jwt_token(user):
    """
    Generate JWT token for user
    
    Args:
        user: User instance
    
    Returns:
        str: JWT token
    """
    payload = {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(days=30),  # 30 days expiry
        'iat': datetime.utcnow()
    }
    
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


def refresh_jwt_token(token):
    """
    Refresh JWT token
    
    Args:
        token: Existing JWT token
    
    Returns:
        str: New JWT token
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=['HS256'],
            options={'verify_exp': False}  # Don't verify expiry for refresh
        )
        
        user_id = payload.get('user_id')
        user = User.objects.get(id=user_id)
        
        if not user.is_active:
            raise AuthenticationFailed('User is inactive')
        
        return generate_jwt_token(user)
    except jwt.InvalidTokenError:
        raise AuthenticationFailed('Invalid token')
    except User.DoesNotExist:
        raise AuthenticationFailed('User not found')


class IsAuthenticatedMobile(BasePermission):
    """
    Permission class for mobile API authentication
    """
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

