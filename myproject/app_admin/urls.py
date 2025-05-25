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
]