"""
Mobile API Views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

from app_admin.models import (
    Bike, BikeRental, BikeReview, Payment, Notification
)
from .serializers import (
    UserSerializer, UserRegistrationSerializer, LoginSerializer,
    BikeSerializer, BikeRentalSerializer, BikeRentalCreateSerializer,
    BikeReviewSerializer, PaymentSerializer, NotificationSerializer
)
from .authentication import generate_jwt_token, refresh_jwt_token, IsAuthenticatedMobile
from app_admin.payment_gateways import get_payment_gateway

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def mobile_register(request):
    """User registration endpoint"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = generate_jwt_token(user)
        return Response({
            'status': 'success',
            'message': 'User registered successfully',
            'token': token,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response({
        'status': 'error',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def mobile_login(request):
    """User login endpoint"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token = generate_jwt_token(user)
        return Response({
            'status': 'success',
            'message': 'Login successful',
            'token': token,
            'user': UserSerializer(user).data
        })
    return Response({
        'status': 'error',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticatedMobile])
def mobile_refresh_token(request):
    """Refresh JWT token endpoint"""
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if not auth_header or not auth_header.startswith('Bearer '):
        return Response({
            'status': 'error',
            'message': 'Token required'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    token = auth_header.split(' ')[1]
    try:
        new_token = refresh_jwt_token(token)
        return Response({
            'status': 'success',
            'token': new_token
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


class BikeViewSet(viewsets.ReadOnlyModelViewSet):
    """Bike viewset"""
    queryset = Bike.objects.filter(is_active=True)
    serializer_class = BikeSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Bike.objects.filter(is_active=True)
        
        # Filter by bike_type
        bike_type = self.request.query_params.get('bike_type', None)
        if bike_type:
            queryset = queryset.filter(bike_type=bike_type)
        
        # Search by name
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        """Check bike availability"""
        bike = self.get_object()
        pickup_date = request.query_params.get('pickup_date')
        return_date = request.query_params.get('return_date')
        quantity = int(request.query_params.get('quantity', 1))
        
        if not pickup_date or not return_date:
            return Response({
                'status': 'error',
                'message': 'pickup_date and return_date required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        from datetime import datetime
        pickup = datetime.strptime(pickup_date, '%Y-%m-%d').date()
        return_d = datetime.strptime(return_date, '%Y-%m-%d').date()
        
        available_qty = bike.get_available_quantity(pickup, return_d)
        is_available = bike.is_available(quantity, pickup, return_d)
        
        return Response({
            'status': 'success',
            'bike_id': bike.id,
            'available_quantity': available_qty,
            'is_available': is_available,
            'quantity_needed': quantity
        })


class BikeRentalViewSet(viewsets.ModelViewSet):
    """Bike rental viewset"""
    serializer_class = BikeRentalSerializer
    permission_classes = [IsAuthenticatedMobile]
    
    def get_queryset(self):
        user = self.request.user
        queryset = BikeRental.objects.filter(user=user)
        
        # Filter by status
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-created_at')
    
    def get_serializer_class(self):
        if self.action == 'create':
            return BikeRentalCreateSerializer
        return BikeRentalSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel rental"""
        rental = self.get_object()
        
        if rental.user != request.user:
            return Response({
                'status': 'error',
                'message': 'Permission denied'
            }, status=status.HTTP_403_FORBIDDEN)
        
        if rental.status not in ['pending', 'approved']:
            return Response({
                'status': 'error',
                'message': 'Cannot cancel rental in this status'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        rental.status = 'cancelled'
        rental.save()
        
        return Response({
            'status': 'success',
            'message': 'Rental cancelled successfully'
        })


class BikeReviewViewSet(viewsets.ModelViewSet):
    """Bike review viewset"""
    serializer_class = BikeReviewSerializer
    permission_classes = [IsAuthenticatedMobile]
    
    def get_queryset(self):
        user = self.request.user
        queryset = BikeReview.objects.filter(user=user)
        
        # Filter by bike
        bike_id = self.request.query_params.get('bike_id', None)
        if bike_id:
            queryset = queryset.filter(bike_id=bike_id)
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_verified=True, is_approved=True)


class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    """Payment viewset"""
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticatedMobile]
    
    def get_queryset(self):
        user = self.request.user
        return Payment.objects.filter(user=user).order_by('-created_at')
    
    @action(detail=False, methods=['post'])
    def create_payment(self, request):
        """Create payment for rental"""
        rental_id = request.data.get('rental_id')
        payment_method = request.data.get('payment_method', 'vnpay')
        
        try:
            rental = BikeRental.objects.get(id=rental_id, user=request.user)
        except BikeRental.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Rental not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Check if already paid
        if Payment.objects.filter(rental=rental, status='completed').exists():
            return Response({
                'status': 'error',
                'message': 'Rental already paid'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create payment
        import uuid
        transaction_id = f"{rental.rental_code}_{uuid.uuid4().hex[:8].upper()}"
        
        payment = Payment.objects.create(
            rental=rental,
            user=request.user,
            amount=rental.total_price or 0,
            payment_method=payment_method,
            transaction_id=transaction_id,
            status='pending',
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        # Get payment gateway
        gateway = get_payment_gateway(payment_method)
        if not gateway:
            payment.status = 'failed'
            payment.save()
            return Response({
                'status': 'error',
                'message': 'Payment method not supported'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create payment URL
        order_info = f"Thanh toan don thue xe {rental.rental_code}"
        payment_url = gateway.create_payment_url(
            amount=payment.amount,
            order_id=transaction_id,
            order_info=order_info,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        if payment_url:
            payment.status = 'processing'
            payment.save()
            
            return Response({
                'status': 'success',
                'payment_id': payment.id,
                'payment_url': payment_url,
                'transaction_id': transaction_id
            })
        else:
            payment.status = 'failed'
            payment.save()
            return Response({
                'status': 'error',
                'message': 'Failed to create payment URL'
            }, status=status.HTTP_400_BAD_REQUEST)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """Notification viewset"""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticatedMobile]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Notification.objects.filter(user=user)
        
        # Filter by read status
        is_read = self.request.query_params.get('is_read', None)
        if is_read is not None:
            queryset = queryset.filter(is_read=is_read.lower() == 'true')
        
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        
        return Response({
            'status': 'success',
            'message': 'Notification marked as read'
        })
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        user = request.user
        Notification.objects.filter(user=user, is_read=False).update(is_read=True)
        
        return Response({
            'status': 'success',
            'message': 'All notifications marked as read'
        })
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get unread notifications count"""
        user = request.user
        count = Notification.objects.filter(user=user, is_read=False).count()
        
        return Response({
            'status': 'success',
            'unread_count': count
        })


@api_view(['GET'])
@permission_classes([IsAuthenticatedMobile])
def mobile_profile(request):
    """Get user profile"""
    serializer = UserSerializer(request.user)
    return Response({
        'status': 'success',
        'user': serializer.data
    })


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticatedMobile])
def mobile_update_profile(request):
    """Update user profile"""
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status': 'success',
            'message': 'Profile updated successfully',
            'user': serializer.data
        })
    return Response({
        'status': 'error',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

