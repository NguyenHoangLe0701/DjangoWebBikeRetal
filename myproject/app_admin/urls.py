from django.urls import path, include
from django.contrib import admin
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.http import JsonResponse
from .models import Store, CustomUser
import json
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard_admin/', views.dashboard_view, name='dashboard'),
    path('map/', views.map_view, name='map'),
    path('du-bao-thoi-tiet/', views.weather, name='weather'),
    path('dich-vu/', views.servers_view, name='dich-vu'),
    path('giai-phap-xe-dap-qua-tang-doanh-nghiep/', views.giai_phap_xe_dap_qua_tang_doanh_nghiep, name='giai-phap-xe-dap-qua-tang-doanh-nghiep'),
    path('bike-rental/', views.bike_rental, name='bike-rental'),
    path('khuyen-mai/', views.khuyen_mai, name='khuyen-mai'),
    path('checkout/', views.check_out, name='checkout'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/', include('allauth.urls')),
    path('traffic-weather/', views.traffic_weather, name='traffic_weather'),
    # API endpoints cho dashboard
    path('api/dashboard/stats/', views.dashboard_stats_api, name='dashboard_stats_api'),
    path('api/dashboard/users/', views.dashboard_users_api, name='dashboard_users_api'),
    path('api/dashboard/bikes/', views.dashboard_bikes_api, name='dashboard_bikes_api'),
    path('api/dashboard/rentals/', views.dashboard_rentals_api, name='dashboard_rentals_api'),
    path('api/dashboard/charts/', views.dashboard_charts_api, name='dashboard_charts_api'),
    path('api/dashboard/bikes/create/', views.dashboard_bike_create_api, name='dashboard_bike_create_api'),
    path('api/dashboard/bikes/<int:bike_id>/delete/', views.dashboard_bike_delete_api, name='dashboard_bike_delete_api'),
    path('api/dashboard/rentals/<int:rental_id>/update-status/', views.dashboard_rental_update_status_api, name='dashboard_rental_update_status_api'),
    path('profile/', views.profile_view, name='profile'),
    path('export-rentals/', views.export_rentals_report, name='export_rentals'),
]