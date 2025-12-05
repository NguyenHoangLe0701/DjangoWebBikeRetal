"""
Integration tests for API endpoints
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import json

from app_admin.models import (
    Bike, BikeRental, BikeReview, Payment
)

User = get_user_model()


class BikeAvailabilityAPITest(TestCase):
    """Test bike availability API"""
    
    def setUp(self):
        self.client = Client()
        self.bike = Bike.objects.create(
            name="Test Bike",
            bike_type="mountain",
            price_per_hour=Decimal('100000'),
            quantity=10,
            is_active=True
        )
    
    def test_check_availability_success(self):
        """Test check availability API success"""
        start_date = (timezone.now().date() + timedelta(days=1)).strftime('%Y-%m-%d')
        end_date = (timezone.now().date() + timedelta(days=5)).strftime('%Y-%m-%d')
        
        url = reverse('check_bike_availability')
        params = {
            'bike_id': self.bike.id,
            'quantity': '2',
            'pickup_date': start_date,
            'return_date': end_date
        }
        
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['bike_id'], self.bike.id)
        self.assertTrue(data['is_available'])
        self.assertEqual(data['available_quantity'], 10)
    
    def test_check_availability_missing_params(self):
        """Test check availability with missing parameters"""
        url = reverse('check_bike_availability')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 400)
    
    def test_check_availability_invalid_dates(self):
        """Test check availability with invalid dates"""
        url = reverse('check_bike_availability')
        params = {
            'bike_id': self.bike.id,
            'quantity': '2',
            'pickup_date': 'invalid-date',
            'return_date': 'invalid-date'
        }
        
        response = self.client.get(url, params)
        self.assertEqual(response.status_code, 400)


class BikeReviewsAPITest(TestCase):
    """Test bike reviews API"""
    
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
        self.review = BikeReview.objects.create(
            user=self.user,
            bike=self.bike,
            rating=5,
            title="Great bike!",
            comment="Very good quality",
            is_approved=True
        )
    
    def test_get_bike_reviews(self):
        """Test get bike reviews API"""
        url = reverse('get_bike_reviews', args=[self.bike.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['bike_id'], self.bike.id)
        self.assertIn('reviews', data)
        self.assertEqual(len(data['reviews']), 1)
        self.assertEqual(data['reviews'][0]['rating'], 5)
    
    def test_get_bike_reviews_not_found(self):
        """Test get reviews for non-existent bike"""
        url = reverse('get_bike_reviews', args=[99999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class SubmitReviewAPITest(TestCase):
    """Test submit review API"""
    
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
            status='completed'
        )
    
    def test_submit_review_success(self):
        """Test submit review successfully"""
        self.client.login(username='testuser', password='testpass123')
        
        url = reverse('submit_review', args=[self.rental.id])
        data = {
            'rating': '5',
            'title': 'Great experience!',
            'comment': 'Very satisfied'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        
        # Check review was created
        review = BikeReview.objects.filter(rental=self.rental).first()
        self.assertIsNotNone(review)
        self.assertEqual(review.rating, 5)
    
    def test_submit_review_requires_login(self):
        """Test submit review requires authentication"""
        url = reverse('submit_review', args=[self.rental.id])
        response = self.client.post(url, {'rating': '5'})
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_submit_review_invalid_rating(self):
        """Test submit review with invalid rating"""
        self.client.login(username='testuser', password='testpass123')
        
        url = reverse('submit_review', args=[self.rental.id])
        data = {
            'rating': '10',  # Invalid rating
            'title': 'Test',
            'comment': 'Test'
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)


class CancelRentalAPITest(TestCase):
    """Test cancel rental API"""
    
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
    
    def test_cancel_rental_success(self):
        """Test cancel rental successfully"""
        self.client.login(username='testuser', password='testpass123')
        
        url = reverse('cancel_rental_api', args=[self.rental.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        
        # Check rental status updated
        self.rental.refresh_from_db()
        self.assertEqual(self.rental.status, 'cancelled')
    
    def test_cancel_rental_requires_login(self):
        """Test cancel rental requires authentication"""
        url = reverse('cancel_rental_api', args=[self.rental.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_cancel_rental_wrong_user(self):
        """Test cancel rental by wrong user"""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        self.client.login(username='otheruser', password='otherpass123')
        
        url = reverse('cancel_rental_api', args=[self.rental.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)  # Not found

