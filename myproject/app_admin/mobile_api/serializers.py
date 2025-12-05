"""
Serializers for Mobile API
"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from app_admin.models import (
    Bike, BikeRental, BikeReview, Payment, Notification
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'full_name', 'phone_number', 'avatar')
        read_only_fields = ('id', 'username', 'email')


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User registration serializer"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'full_name', 'phone_number')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    """Login serializer"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
            attrs['user'] = user
        else:
            raise serializers.ValidationError('Must include username and password')
        
        return attrs


class BikeSerializer(serializers.ModelSerializer):
    """Bike serializer"""
    bike_type_display = serializers.CharField(source='get_bike_type_display', read_only=True)
    average_rating = serializers.SerializerMethodField()
    rating_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Bike
        fields = (
            'id', 'name', 'bike_type', 'bike_type_display',
            'price_per_hour', 'quantity', 'image', 'description',
            'is_active', 'average_rating', 'rating_count', 'created_at'
        )
    
    def get_average_rating(self, obj):
        return obj.get_average_rating()
    
    def get_rating_count(self, obj):
        return obj.get_rating_count()


class BikeRentalSerializer(serializers.ModelSerializer):
    """Bike rental serializer"""
    bike = BikeSerializer(read_only=True)
    bike_type_display = serializers.CharField(source='get_bike_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    has_paid = serializers.SerializerMethodField()
    
    class Meta:
        model = BikeRental
        fields = (
            'id', 'rental_code', 'bike', 'full_name', 'email', 'phone',
            'bike_type', 'bike_type_display', 'quantity', 'pickup_date',
            'return_date', 'message', 'status', 'status_display',
            'total_price', 'created_at', 'has_paid'
        )
        read_only_fields = ('rental_code', 'created_at', 'total_price')
    
    def get_has_paid(self, obj):
        return Payment.objects.filter(rental=obj, status='completed').exists()


class BikeRentalCreateSerializer(serializers.ModelSerializer):
    """Bike rental creation serializer"""
    
    class Meta:
        model = BikeRental
        fields = (
            'bike', 'full_name', 'email', 'phone', 'bike_type',
            'quantity', 'pickup_date', 'return_date', 'message'
        )
    
    def validate(self, attrs):
        pickup_date = attrs.get('pickup_date')
        return_date = attrs.get('return_date')
        
        if pickup_date and return_date:
            if return_date <= pickup_date:
                raise serializers.ValidationError('Return date must be after pickup date')
            if (return_date - pickup_date).days > 30:
                raise serializers.ValidationError('Rental period cannot exceed 30 days')
        
        return attrs


class BikeReviewSerializer(serializers.ModelSerializer):
    """Bike review serializer"""
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    bike_name = serializers.CharField(source='bike.name', read_only=True)
    
    class Meta:
        model = BikeReview
        fields = (
            'id', 'user', 'user_name', 'bike', 'bike_name',
            'rental', 'rating', 'title', 'comment',
            'is_verified', 'is_approved', 'created_at'
        )
        read_only_fields = ('user', 'is_verified', 'is_approved', 'created_at')


class PaymentSerializer(serializers.ModelSerializer):
    """Payment serializer"""
    payment_method_display = serializers.CharField(source='get_payment_method_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Payment
        fields = (
            'id', 'rental', 'amount', 'payment_method', 'payment_method_display',
            'transaction_id', 'gateway_transaction_id', 'status', 'status_display',
            'created_at', 'paid_at'
        )
        read_only_fields = ('transaction_id', 'created_at', 'paid_at')


class NotificationSerializer(serializers.ModelSerializer):
    """Notification serializer"""
    notification_type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    
    class Meta:
        model = Notification
        fields = (
            'id', 'notification_type', 'notification_type_display',
            'message', 'link', 'is_read', 'created_at'
        )
        read_only_fields = ('created_at',)

