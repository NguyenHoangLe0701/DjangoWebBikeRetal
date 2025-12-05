"""
Unit tests for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import random
import string

from app_admin.models import (
    Bike, BikeRental, BikeReview, Payment, 
    Notification, NotificationPreference, AuditLog
)

User = get_user_model()


class BikeModelTest(TestCase):
    """Test Bike model"""
    
    def setUp(self):
        self.bike = Bike.objects.create(
            name="Mountain Bike Pro",
            bike_type="mountain",
            price_per_hour=Decimal('100000'),
            quantity=10,
            description="Test bike",
            is_active=True
        )
    
    def test_bike_creation(self):
        """Test bike creation"""
        self.assertEqual(self.bike.name, "Mountain Bike Pro")
        self.assertEqual(self.bike.bike_type, "mountain")
        self.assertEqual(self.bike.price_per_hour, Decimal('100000'))
        self.assertEqual(self.bike.quantity, 10)
        self.assertTrue(self.bike.is_active)
    
    def test_bike_str(self):
        """Test bike string representation"""
        self.assertIn("Mountain Bike Pro", str(self.bike))
        self.assertIn("Xe đạp leo núi", str(self.bike))
    
    def test_get_average_rating(self):
        """Test average rating calculation"""
        # No reviews yet
        self.assertEqual(self.bike.get_average_rating(), 0.0)
        
        # Create reviews
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        BikeReview.objects.create(
            user=user,
            bike=self.bike,
            rating=5,
            is_approved=True
        )
        BikeReview.objects.create(
            user=user,
            bike=self.bike,
            rating=4,
            is_approved=True
        )
        
        avg = self.bike.get_average_rating()
        self.assertEqual(avg, 4.5)
    
    def test_get_rating_count(self):
        """Test rating count"""
        self.assertEqual(self.bike.get_rating_count(), 0)
        
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        BikeReview.objects.create(
            user=user,
            bike=self.bike,
            rating=5,
            is_approved=True
        )
        
        self.assertEqual(self.bike.get_rating_count(), 1)
    
    def test_get_available_quantity(self):
        """Test available quantity calculation"""
        # No rentals, should return full quantity
        available = self.bike.get_available_quantity()
        self.assertEqual(available, 10)
        
        # With date range
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=5)
        available = self.bike.get_available_quantity(start_date, end_date)
        self.assertEqual(available, 10)
    
    def test_is_available(self):
        """Test availability check"""
        start_date = timezone.now().date()
        end_date = start_date + timedelta(days=5)
        
        # Should be available for 5 bikes
        self.assertTrue(self.bike.is_available(5, start_date, end_date))
        
        # Should not be available for 15 bikes
        self.assertFalse(self.bike.is_available(15, start_date, end_date))
    
    def test_is_low_stock(self):
        """Test low stock check"""
        self.bike.quantity = 2
        self.bike.save()
        self.assertTrue(self.bike.is_low_stock(threshold=3))
        
        self.bike.quantity = 5
        self.bike.save()
        self.assertFalse(self.bike.is_low_stock(threshold=3))
    
    def test_is_out_of_stock(self):
        """Test out of stock check"""
        self.bike.quantity = 0
        self.bike.save()
        self.assertTrue(self.bike.is_out_of_stock())
        
        self.bike.quantity = 1
        self.bike.save()
        self.assertFalse(self.bike.is_out_of_stock())


class BikeRentalModelTest(TestCase):
    """Test BikeRental model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.bike = Bike.objects.create(
            name="Test Bike",
            bike_type="mountain",
            price_per_hour=Decimal('100000'),
            quantity=10
        )
        self.rental = BikeRental.objects.create(
            user=self.user,
            bike=self.bike,
            full_name="Test User",
            email="test@example.com",
            phone="0123456789",
            bike_type="mountain",
            quantity=2,
            pickup_date=timezone.now().date() + timedelta(days=1),
            return_date=timezone.now().date() + timedelta(days=5),
            status='pending'
        )
    
    def test_rental_creation(self):
        """Test rental creation"""
        self.assertEqual(self.rental.user, self.user)
        self.assertEqual(self.rental.bike, self.bike)
        self.assertEqual(self.rental.full_name, "Test User")
        self.assertEqual(self.rental.quantity, 2)
        self.assertEqual(self.rental.status, 'pending')
        self.assertIsNotNone(self.rental.rental_code)
        self.assertEqual(len(self.rental.rental_code), 8)
    
    def test_rental_code_generation(self):
        """Test rental code is auto-generated"""
        rental2 = BikeRental.objects.create(
            user=self.user,
            bike=self.bike,
            full_name="Test User 2",
            email="test2@example.com",
            phone="0123456788",
            bike_type="mountain",
            quantity=1,
            pickup_date=timezone.now().date() + timedelta(days=1),
            return_date=timezone.now().date() + timedelta(days=3)
        )
        self.assertIsNotNone(rental2.rental_code)
        self.assertNotEqual(self.rental.rental_code, rental2.rental_code)
    
    def test_total_price_calculation(self):
        """Test total price calculation"""
        # 5 days = 5 * 24 = 120 hours
        # 120 hours * 100000 VND/hour * 2 bikes = 24,000,000 VND
        expected_price = Decimal('24000000')
        self.assertEqual(self.rental.total_price, expected_price)
    
    def test_rental_str(self):
        """Test rental string representation"""
        self.assertIn("Test User", str(self.rental))
        self.assertIn(self.rental.rental_code, str(self.rental))


class BikeReviewModelTest(TestCase):
    """Test BikeReview model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.bike = Bike.objects.create(
            name="Test Bike",
            bike_type="mountain",
            price_per_hour=Decimal('100000'),
            quantity=10
        )
        self.review = BikeReview.objects.create(
            user=self.user,
            bike=self.bike,
            rating=5,
            title="Great bike!",
            comment="Very good quality",
            is_verified=True,
            is_approved=True
        )
    
    def test_review_creation(self):
        """Test review creation"""
        self.assertEqual(self.review.user, self.user)
        self.assertEqual(self.review.bike, self.bike)
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.title, "Great bike!")
        self.assertTrue(self.review.is_verified)
        self.assertTrue(self.review.is_approved)
    
    def test_review_str(self):
        """Test review string representation"""
        self.assertIn("testuser", str(self.review))
        self.assertIn("Test Bike", str(self.review))
        self.assertIn("5", str(self.review))


class PaymentModelTest(TestCase):
    """Test Payment model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.bike = Bike.objects.create(
            name="Test Bike",
            bike_type="mountain",
            price_per_hour=Decimal('100000'),
            quantity=10
        )
        self.rental = BikeRental.objects.create(
            user=self.user,
            bike=self.bike,
            full_name="Test User",
            email="test@example.com",
            phone="0123456789",
            bike_type="mountain",
            quantity=2,
            pickup_date=timezone.now().date() + timedelta(days=1),
            return_date=timezone.now().date() + timedelta(days=5),
            status='pending'
        )
        self.payment = Payment.objects.create(
            rental=self.rental,
            user=self.user,
            amount=Decimal('24000000'),
            payment_method='vnpay',
            transaction_id='TEST123456',
            status='pending'
        )
    
    def test_payment_creation(self):
        """Test payment creation"""
        self.assertEqual(self.payment.rental, self.rental)
        self.assertEqual(self.payment.user, self.user)
        self.assertEqual(self.payment.amount, Decimal('24000000'))
        self.assertEqual(self.payment.payment_method, 'vnpay')
        self.assertEqual(self.payment.status, 'pending')
    
    def test_payment_str(self):
        """Test payment string representation"""
        self.assertIn(self.rental.rental_code, str(self.payment))
        self.assertIn("VNPay", str(self.payment))
    
    def test_mark_as_completed(self):
        """Test mark payment as completed"""
        self.payment.mark_as_completed()
        self.assertEqual(self.payment.status, 'completed')
        self.assertIsNotNone(self.payment.paid_at)
        
        # Check rental status updated
        self.rental.refresh_from_db()
        self.assertEqual(self.rental.status, 'approved')


class NotificationModelTest(TestCase):
    """Test Notification model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.notification = Notification.objects.create(
            user=self.user,
            notification_type='rental_created',
            message="Your rental has been created",
            link="/customer-dashboard/"
        )
    
    def test_notification_creation(self):
        """Test notification creation"""
        self.assertEqual(self.notification.user, self.user)
        self.assertEqual(self.notification.notification_type, 'rental_created')
        self.assertFalse(self.notification.is_read)
    
    def test_notification_str(self):
        """Test notification string representation"""
        self.assertIn("rental_created", str(self.notification))
        self.assertIn("testuser", str(self.notification))


class NotificationPreferenceModelTest(TestCase):
    """Test NotificationPreference model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.preference = NotificationPreference.objects.create(
            user=self.user,
            email_enabled=True,
            sms_enabled=False,
            in_app_enabled=True
        )
    
    def test_preference_creation(self):
        """Test preference creation"""
        self.assertEqual(self.preference.user, self.user)
        self.assertTrue(self.preference.email_enabled)
        self.assertFalse(self.preference.sms_enabled)
        self.assertTrue(self.preference.in_app_enabled)

