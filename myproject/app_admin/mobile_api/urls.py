"""
Mobile API URLs
"""
from django.urls import path, include

try:
    from rest_framework.routers import DefaultRouter
    from . import views
    REST_FRAMEWORK_AVAILABLE = True
    
    # Initialize router if REST Framework is available
    router = DefaultRouter()
    try:
        router.register(r'bikes', views.BikeViewSet, basename='bike')
        router.register(r'rentals', views.BikeRentalViewSet, basename='rental')
        router.register(r'reviews', views.BikeReviewViewSet, basename='review')
        router.register(r'payments', views.PaymentViewSet, basename='payment')
        router.register(r'notifications', views.NotificationViewSet, basename='notification')
        router_urls = router.urls
    except (AttributeError, NameError):
        # Views not available (REST Framework not installed or views not defined)
        router_urls = []
except ImportError:
    # REST Framework not installed
    REST_FRAMEWORK_AVAILABLE = False
    router_urls = []
    from . import views

urlpatterns = [
    # Authentication
    path('auth/register/', views.mobile_register, name='mobile_register'),
    path('auth/login/', views.mobile_login, name='mobile_login'),
    path('auth/refresh/', views.mobile_refresh_token, name='mobile_refresh_token'),
    
    # Profile
    path('profile/', views.mobile_profile, name='mobile_profile'),
    path('profile/update/', views.mobile_update_profile, name='mobile_update_profile'),
    
    # API endpoints (only if REST Framework is available)
] + router_urls
