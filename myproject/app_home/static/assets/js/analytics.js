/**
 * Analytics Tracking JavaScript
 * Handles custom events, conversions, and user behavior tracking
 */

// Initialize analytics
(function() {
    'use strict';
    
    // Check if gtag is available
    if (typeof gtag === 'undefined') {
        console.warn('Google Analytics not loaded');
        return;
    }
    
    // Track page views with custom dimensions
    function trackPageView(pageName, pageCategory) {
        if (typeof gtag !== 'undefined') {
            gtag('event', 'page_view', {
                'page_title': pageName,
                'page_location': window.location.href,
                'page_path': window.location.pathname,
                'custom_map': {
                    'dimension1': pageCategory || 'general'
                }
            });
        }
    }
    
    // Track rental booking (conversion)
    function trackRentalBooking(rentalData) {
        if (typeof gtag !== 'undefined') {
            gtag('event', 'rental_booking', {
                'event_category': 'Ecommerce',
                'event_label': 'Bike Rental',
                'value': rentalData.total_price || 0,
                'currency': 'VND',
                'items': [{
                    'id': rentalData.rental_code,
                    'name': rentalData.bike_type || 'Bike Rental',
                    'category': rentalData.bike_type || 'Bike',
                    'quantity': rentalData.quantity || 1,
                    'price': rentalData.total_price || 0
                }]
            });
            
            // Enhanced Ecommerce - Purchase
            gtag('event', 'purchase', {
                'transaction_id': rentalData.rental_code,
                'value': rentalData.total_price || 0,
                'currency': 'VND',
                'items': [{
                    'id': rentalData.rental_code,
                    'name': rentalData.bike_type || 'Bike Rental',
                    'category': rentalData.bike_type || 'Bike',
                    'quantity': rentalData.quantity || 1,
                    'price': rentalData.total_price || 0
                }]
            });
        }
    }
    
    // Track search events
    function trackSearch(searchQuery, resultsCount) {
        if (typeof gtag !== 'undefined') {
            gtag('event', 'search', {
                'search_term': searchQuery,
                'results_count': resultsCount || 0
            });
        }
    }
    
    // Track filter events
    function trackFilter(filterType, filterValue) {
        if (typeof gtag !== 'undefined') {
            gtag('event', 'filter', {
                'filter_type': filterType,
                'filter_value': filterValue
            });
        }
    }
    
    // Track bike view
    function trackBikeView(bikeId, bikeName, bikeType) {
        if (typeof gtag !== 'undefined') {
            gtag('event', 'view_item', {
                'items': [{
                    'id': bikeId,
                    'name': bikeName,
                    'category': bikeType
                }]
            });
        }
    }
    
    // Track form submissions
    function trackFormSubmission(formType, success) {
        if (typeof gtag !== 'undefined') {
            gtag('event', 'form_submission', {
                'form_type': formType,
                'success': success
            });
        }
    }
    
    // Track button clicks
    function trackButtonClick(buttonName, buttonLocation) {
        if (typeof gtag !== 'undefined') {
            gtag('event', 'button_click', {
                'button_name': buttonName,
                'button_location': buttonLocation || 'unknown'
            });
        }
    }
    
    // Track user engagement
    function trackEngagement(action, category, label) {
        if (typeof gtag !== 'undefined') {
            gtag('event', action, {
                'event_category': category,
                'event_label': label
            });
        }
    }
    
    // Track time on page
    let timeOnPageStart = Date.now();
    window.addEventListener('beforeunload', function() {
        if (typeof gtag !== 'undefined') {
            const timeOnPage = Math.round((Date.now() - timeOnPageStart) / 1000);
            if (timeOnPage > 0) {
                gtag('event', 'time_on_page', {
                    'value': timeOnPage,
                    'event_category': 'Engagement'
                });
            }
        }
    });
    
    // Track scroll depth
    let maxScroll = 0;
    window.addEventListener('scroll', function() {
        const scrollPercent = Math.round(
            (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100
        );
        if (scrollPercent > maxScroll) {
            maxScroll = scrollPercent;
            // Track at 25%, 50%, 75%, 100%
            if ([25, 50, 75, 100].includes(scrollPercent) && typeof gtag !== 'undefined') {
                gtag('event', 'scroll', {
                    'scroll_depth': scrollPercent,
                    'event_category': 'Engagement'
                });
            }
        }
    });
    
    // Export functions to global scope
    window.analytics = {
        trackPageView: trackPageView,
        trackRentalBooking: trackRentalBooking,
        trackSearch: trackSearch,
        trackFilter: trackFilter,
        trackBikeView: trackBikeView,
        trackFormSubmission: trackFormSubmission,
        trackButtonClick: trackButtonClick,
        trackEngagement: trackEngagement
    };
    
    // Auto-track page view on load
    document.addEventListener('DOMContentLoaded', function() {
        const pageName = document.title;
        const pageCategory = document.body.getAttribute('data-page-category') || 'general';
        trackPageView(pageName, pageCategory);
    });
})();

