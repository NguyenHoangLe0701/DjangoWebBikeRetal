"""
Unit tests for views
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import json

from app_admin.models import (
    Bike, BikeRental, BikeReview, Payment, 
    Notification, NotificationPreference
)

User = get_user_model()


class HomeViewTest(TestCase):
    """Test home view"""
    
    def setUp(self):
        self.client = Client()
    
    def test_home_view(self):
        """Test home page loads"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')


class BikeRentalViewTest(TestCase):
    """Test bike rental view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.bike = Bike.objects.create(
            name="Test Bike",
            bike_type="mountain",
            price_per_hour=Decimal('100000'),
            quantity=10,
            is_active=True
        )
    
    def test_bike_rental_get(self):
        """Test GET request to bike rental page"""
        response = self.client.get(reverse('bike-rental'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/bike-rental.html')
    
    def test_bike_rental_post_success(self):
        """Test successful bike rental POST"""
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'full_name': 'Test User',
            'email': 'test@example.com',
            'phone': '0123456789',
            'bike_type': 'mountain',
            'quantity': '2',
            'pickup_date': (timezone.now().date() + timedelta(days=1)).strftime('%Y-%m-%d'),
            'return_date': (timezone.now().date() + timedelta(days=5)).strftime('%Y-%m-%d'),
            'message': 'Test message'
        }
        
        response = self.client.post(reverse('bike-rental'), data)
        self.assertEqual(response.status_code, 200)
        
        # Check rental was created
        rental = BikeRental.objects.filter(user=self.user).first()
        self.assertIsNotNone(rental)
        self.assertEqual(rental.full_name, 'Test User')
        self.assertEqual(rental.quantity, 2)
    
    def test_bike_rental_post_invalid_data(self):
        """Test bike rental POST with invalid data"""
        self.client.login(username='testuser', password='testpass123')
        
        data = {
            'full_name': '',  # Missing required field
            'email': 'test@example.com',
            'phone': '0123456789',
            'bike_type': 'mountain',
            'quantity': '2',
            'pickup_date': (timezone.now().date() + timedelta(days=1)).strftime('%Y-%m-%d'),
            'return_date': (timezone.now().date() + timedelta(days=5)).strftime('%Y-%m-%d'),
        }
        
        response = self.client.post(reverse('bike-rental'), data)
        self.assertEqual(response.status_code, 200)  # Returns form with errors


class CustomerDashboardTest(TestCase):
    """Test customer dashboard"""
    
    def setUp(self):
        self.client = Client()
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
    
    def test_customer_dashboard_requires_login(self):
        """Test dashboard requires authentication"""
        response = self.client.get(reverse('customer_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_customer_dashboard_authenticated(self):
        """Test dashboard for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('customer_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/customer_dashboard.html')
        self.assertIn(self.rental, response.context['rentals'])
    
    def test_customer_dashboard_stats(self):
        """Test dashboard stats"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('customer_dashboard'))
        self.assertEqual(response.status_code, 200)
        
        stats = response.context['stats']
        self.assertEqual(stats['total_rentals'], 1)
        self.assertEqual(stats['pending_rentals'], 1)


class DashboardAPITest(TestCase):
    """Test dashboard API endpoints"""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpass123'
        )
    
    def test_dashboard_stats_api_requires_staff(self):
        """Test dashboard stats API requires staff"""
        self.client.login(username='user', password='userpass123')
        response = self.client.get(reverse('dashboard_stats_api'))
        self.assertEqual(response.status_code, 403)
    
    def test_dashboard_stats_api_staff(self):
        """Test dashboard stats API for staff"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('dashboard_stats_api'))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('totalCustomers', data)
        self.assertIn('availableBicycles', data)
        self.assertIn('activeRentals', data)
        self.assertIn('monthlyRentals', data)
        self.assertIn('monthlyRevenue', data)


class NotificationAPITest(TestCase):
    """Test notification API endpoints"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.notification = Notification.objects.create(
            user=self.user,
            notification_type='rental_created',
            message="Test notification",
            link="/customer-dashboard/"
        )
    
    def test_get_notifications_requires_login(self):
        """Test get notifications requires authentication"""
        response = self.client.get(reverse('get_notifications'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_get_notifications(self):
        """Test get notifications"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('get_notifications'))
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('notifications', data)
        self.assertIn('unread_count', data)
        self.assertEqual(len(data['notifications']), 1)
    
    def test_mark_notification_read(self):
        """Test mark notification as read"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('mark_notification_read', args=[self.notification.id])
        )
        self.assertEqual(response.status_code, 200)
        
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)
    
    def test_mark_all_notifications_read(self):
        """Test mark all notifications as read"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('mark_all_notifications_read'))
        self.assertEqual(response.status_code, 200)
        
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)

