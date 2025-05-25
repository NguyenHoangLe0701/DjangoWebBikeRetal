from django.shortcuts import render,redirect
from .models import TrafficReport


from django.core.cache import cache
from django.http import JsonResponse

from app_admin.models import Store, Article
#from .models import Product
import json
from django.views.decorators.cache import cache_page
from django.views.decorators.clickjacking import xframe_options_exempt
#dashboard
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse
from django.db import models
#send email
from django.core.mail import send_mail
#countdown
from datetime import datetime, timedelta
from django.utils import timezone
#information
from .models import Article
#login

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, ForgotPasswordForm
from .models import CustomUser
from django.contrib import messages
#Thuê xe đạp
from .models import BikeRental
from django.template.loader import render_to_string
from django.conf import settings

# Create your views here.
#def home(request):
    #return render(request, 'home/home.html')

def map_view(request):
    return render(request, 'home/map.html')

def servers_view(request):
    return render(request, 'home/dich-vu.html')

def giai_phap_xe_dap_qua_tang_doanh_nghiep(request):
    return render(request, 'home/giai-phap-xe-dap-qua-tang-doanh-nghiep.html')

def bike_rental(request):
    return render(request, 'home/bike-rental.html')

def check_out(request):
    return render(request, 'home/checkout.html')

#weather
def weather(request):
    import requests
    from datetime import datetime
    import pytz

    # Cấu hình API
    API_KEY = '3f5bd7cba7b41690c98d983ab918e180' 
    CITY = 'Ho Chi Minh City'
    LAT = 10.7757  # Vĩ độ của HCM
    LON = 106.7004  # Kinh độ của HCM
    
    # Lấy dữ liệu thời tiết từ OpenWeatherMap One Call 3.0
    weather_url = f'https://api.openweathermap.org/data/3.0/onecall?lat={LAT}&lon={LON}&exclude=minutely&units=metric&appid={API_KEY}'
    
    try:
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()
        
        # Xử lý dữ liệu thời tiết
        forecast = []
        if 'daily' in weather_data:
            for day in weather_data['daily'][:7]:  # Lấy 7 ngày
                forecast.append({
                    'date': datetime.fromtimestamp(day['dt'], tz=pytz.timezone('Asia/Ho_Chi_Minh')).strftime('%d/%m/%Y'),
                    'temp': round(day['temp']['day']),
                    'feels_like': round(day['feels_like']['day']),
                    'humidity': day['humidity'],
                    'wind_speed': round(day['wind_speed'], 1),
                    'description': day['weather'][0]['description'],
                    'icon': day['weather'][0]['icon'],
                    'pop': round(day['pop'] * 100),  # Xác suất mưa
                    'rain': round(day.get('rain', 0), 1),  # Lượng mưa
                    'pressure': day['pressure'],
                    'clouds': day['clouds'],
                    'uvi': round(day['uvi'], 1),  # Chỉ số UV
                    'sunrise': datetime.fromtimestamp(day['sunrise'], tz=pytz.timezone('Asia/Ho_Chi_Minh')).strftime('%H:%M'),
                    'sunset': datetime.fromtimestamp(day['sunset'], tz=pytz.timezone('Asia/Ho_Chi_Minh')).strftime('%H:%M')
                })

        # Lấy dữ liệu giao thông từ TomTom
        traffic_url = f'https://api.tomtom.com/traffic/services/4/incidentDetails/s3/{LAT},{LON}/10/0/true/false/true/true/true/true?key=YOUR_TOMTOM_KEY'
        traffic_response = requests.get(traffic_url)
        traffic_data = traffic_response.json()

        traffic_incidents = []
        if 'tm' in traffic_data and 'poi' in traffic_data['tm']:
            for incident in traffic_data['tm']['poi']:
                traffic_incidents.append({
                    'type': incident.get('ic', 'Sự cố giao thông'),
                    'description': incident.get('d', 'Không có mô tả'),
                    'location': incident.get('l', 'Không xác định'),
                    'severity': incident.get('s', 0)
                })

        context = {
            'forecast': forecast,
            'traffic_incidents': traffic_incidents,
            'city': CITY
        }
        
        return render(request, 'home/du-bao-thoi-tiet.html', context)
        
    except Exception as e:
        return render(request, 'home/du-bao-thoi-tiet.html', {
            'error': f'Không thể lấy dữ liệu thời tiết: {str(e)}',
            'city': CITY
        })

def traffic_weather(request):
    """
    View function cho trang traffic-weather
    Sử dụng lại logic từ function weather
    """
    return weather(request)

# Giả sử bạn đặt thời gian bắt đầu khuyến mãi cố định (hoặc sinh động)
START_TIME = datetime(2025, 5, 16, 9, 48, 0)  # YYYY, MM, DD, HH, MM, SS
PROMO_DURATION = timedelta(hours=24)

# Cấu hình thời gian bắt đầu và thời gian khuyến mãi
#START_TIME = datetime(2025, 5, 16, 12, 0, 0)  # Bắt đầu từ 12:00 trưa
#PROMO_DURATION = timedelta(hours=1)  # Khuyến mãi kéo dài 1 tiếng

def khuyen_mai(request):
    now = datetime.now()
    end_time = START_TIME + PROMO_DURATION
    remaining = end_time - now

    if remaining.total_seconds() < 0:
        remaining_seconds = 0
    else:
        remaining_seconds = int(remaining.total_seconds())

    context = {
        'remaining_seconds': remaining_seconds
    }
    return render(request, 'home/khuyen-mai.html', context)
#cowndown


@cache_page(60 * 15)# Cache cho 15 phút
def dashboard_view(request):
    return render(request, 'home/dashboard_admin.html', {'request': request})

#@cache_page(60)  # Cache cho 60 giây
#def product_list(request):
  #  cached_products = cache.get('products')
   # if cached_products is not None:
    #    return JsonResponse(cached_products, safe=False)

   # products = list(Product.objects.all().values())
    #cache.set('products', products, timeout=60)
    #return JsonResponse(products, safe=False)


#Send email
def send_rental_confirmation(user_email, rental_id):
    subject = 'Xác nhận đơn thuê xe'
    message = f'Đơn thuê #{rental_id} của bạn đã được xác nhận. Cảm ơn bạn đã sử dụng dịch vụ!'
    send_mail(subject, message, 'your-email@gmail.com', [user_email])


# 
def home_view(request):
    stores = Store.objects.all()
    articles = Article.objects.all().order_by('-publish_date')[:10]
    context = {
        'stores': stores,
        'articles': articles,
        'page_title': 'Trang Chủ',
    }
    return render(request, 'home/home.html', context)




#login
# Trang chủ (để kiểm tra header)
#def home(request):
    #return render(request, 'header.html')

# Đăng nhập
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Đăng nhập thành công!')
                return redirect('home')  # Chuyển hướng về trang home
            else:
                messages.error(request, 'Email hoặc mật khẩu không đúng!')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'includes/overlays.html', {'form': form, 'overlay_type': 'login'})

# Đăng ký
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Đăng ký thành công!')
            return redirect('home/home.html')
    else:
        form = CustomUserCreationForm()
    return render(request, 'includes/overlays.html', {'form': form, 'overlay_type': 'register'})

# Lấy lại mật khẩu
def forgot_password_view(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        try:
            user = CustomUser.objects.get(phone_number=phone_number)
            # Gửi email reset password
            messages.success(request, 'Hướng dẫn đặt lại mật khẩu đã được gửi đến email của bạn!')
            return redirect('home/home.html')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Số điện thoại không tồn tại trong hệ thống!')
    return render(request, 'includes/overlays.html', {'overlay_type': 'forgot_password'})

# Đăng xuất
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Đăng xuất thành công!')
    return redirect('home/home.html')


#Dự báo thời tiết



#Thuê xe đạp
@csrf_exempt
def bike_rental(request):
    if request.method == 'POST':
        try:
            # Validate required fields
            required_fields = ['full_name', 'email', 'phone', 'bike_type', 'quantity', 'pickup_date', 'return_date']
            for field in required_fields:
                if not request.POST.get(field):
                    return JsonResponse({
                        'status': 'error',
                        'message': f'Vui lòng điền đầy đủ thông tin {field}'
                    }, status=400)

            # Validate dates
            try:
                pickup_date = datetime.strptime(request.POST.get('pickup_date'), '%Y-%m-%d').date()
                return_date = datetime.strptime(request.POST.get('return_date'), '%Y-%m-%d').date()
                
                if pickup_date < datetime.now().date():
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Ngày nhận xe không được trong quá khứ'
                    }, status=400)
                
                if return_date <= pickup_date:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Ngày trả xe phải sau ngày nhận xe'
                    }, status=400)
                
                if (return_date - pickup_date).days > 30:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Thời gian thuê xe không được vượt quá 30 ngày'
                    }, status=400)
            except ValueError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Định dạng ngày không hợp lệ'
                }, status=400)

            # Validate phone number
            phone = request.POST.get('phone')
            if not phone.isdigit() or len(phone) != 10:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Số điện thoại phải có 10 chữ số'
                }, status=400)

            # Validate quantity
            try:
                quantity = int(request.POST.get('quantity'))
                if quantity < 1 or quantity > 10:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Số lượng xe phải từ 1 đến 10'
                    }, status=400)
            except ValueError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Số lượng xe không hợp lệ'
                }, status=400)

            # Create new rental record
            rental = BikeRental.objects.create(
                full_name=request.POST.get('full_name'),
                email=request.POST.get('email'),
                phone=phone,
                bike_type=request.POST.get('bike_type'),
                quantity=quantity,
                pickup_date=pickup_date,
                return_date=return_date,
                message=request.POST.get('message', '')
            )

            # Prepare email content
            context = {
                'rental': rental,
                'bike_type_display': dict(BikeRental.BIKE_TYPES)[rental.bike_type]
            }
            email_html_message = render_to_string('home/email/rental_confirmation.html', context)
            email_plain_message = render_to_string('home/email/rental_confirmation.txt', context)

            # Send confirmation email
            try:
                send_mail(
                    subject=f'Xác nhận đặt xe - Mã số: {rental.rental_code}',
                    message=email_plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[rental.email],
                    html_message=email_html_message,
                    fail_silently=False,
                )
            except Exception as e:
                # Log email error but don't fail the rental
                print(f"Failed to send email: {str(e)}")

            return JsonResponse({
                'status': 'success',
                'message': 'Đặt xe thành công! Vui lòng kiểm tra email của bạn.',
                'rental_code': rental.rental_code
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Có lỗi xảy ra: {str(e)}'
            }, status=400)

    return render(request, 'home/bike-rental.html') 