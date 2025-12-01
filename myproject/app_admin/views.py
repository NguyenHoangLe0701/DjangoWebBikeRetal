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
from .models import BikeRental, Bike, CustomUser
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import timedelta

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


@login_required
@cache_page(60 * 15)# Cache cho 15 phút
def dashboard_view(request):
    if not request.user.is_staff:
        messages.error(request, 'Bạn không có quyền truy cập trang này.')
        return redirect('home')
    return render(request, 'home/dashboard_admin.html', {'request': request})

# API endpoints cho dashboard
@login_required
def dashboard_stats_api(request):
    """API trả về thống kê tổng quan"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    now = timezone.now()
    today = now.date()
    this_month_start = today.replace(day=1)
    
    # Thống kê
    total_customers = CustomUser.objects.filter(is_staff=False).count()
    total_bikes = Bike.objects.filter(is_active=True).aggregate(Sum('quantity'))['quantity__sum'] or 0
    active_rentals = BikeRental.objects.filter(
        status__in=['approved', 'renting'],
        return_date__gte=today
    ).count()
    
    # Đơn thuê trong tháng
    monthly_rentals = BikeRental.objects.filter(created_at__gte=this_month_start).count()
    
    # Doanh thu trong tháng
    monthly_revenue = BikeRental.objects.filter(
        created_at__gte=this_month_start,
        status__in=['completed', 'renting']
    ).aggregate(Sum('total_price'))['total_price__sum'] or 0
    
    return JsonResponse({
        'totalCustomers': total_customers,
        'availableBicycles': total_bikes,
        'activeRentals': active_rentals,
        'monthlyRentals': monthly_rentals,
        'monthlyRevenue': float(monthly_revenue) if monthly_revenue else 0,
    })

@login_required
def dashboard_users_api(request):
    """API trả về danh sách users"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    users = CustomUser.objects.filter(is_staff=False).values(
        'id', 'username', 'email', 'phone_number', 'full_name', 'date_joined'
    )[:100]  # Giới hạn 100 users
    
    return JsonResponse({
        'users': list(users)
    })

@login_required
def dashboard_bikes_api(request):
    """API trả về danh sách bikes"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    bikes = Bike.objects.all().values(
        'id', 'name', 'bike_type', 'price_per_hour', 'quantity', 'is_active'
    )
    
    return JsonResponse({
        'bikes': list(bikes)
    })

@login_required
def dashboard_rentals_api(request):
    """API trả về danh sách rentals"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    rentals = BikeRental.objects.select_related('bike', 'user').all().order_by('-created_at')[:100]
    
    rentals_data = []
    for rental in rentals:
        rentals_data.append({
            'id': rental.id,
            'rental_code': rental.rental_code,
            'user': rental.full_name,
            'email': rental.email,
            'phone': rental.phone,
            'bike': rental.bike.name if rental.bike else rental.get_bike_type_display(),
            'bike_type': rental.get_bike_type_display(),
            'quantity': rental.quantity,
            'pickup_date': rental.pickup_date.strftime('%Y-%m-%d'),
            'return_date': rental.return_date.strftime('%Y-%m-%d'),
            'startTime': rental.pickup_date.strftime('%Y-%m-%d %H:%M'),
            'status': rental.get_status_display(),
            'status_code': rental.status,
            'total_price': float(rental.total_price) if rental.total_price else 0,
            'created_at': rental.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        })
    
    return JsonResponse({
        'rentals': rentals_data
    })

@login_required
@csrf_exempt
def dashboard_bike_create_api(request):
    """API tạo/sửa bike"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            bike_id = data.get('id')
            
            if bike_id:
                # Update existing bike
                bike = Bike.objects.get(id=bike_id)
                bike.name = data.get('model', bike.name)
                bike.bike_type = data.get('type', bike.bike_type)
                bike.price_per_hour = data.get('price', bike.price_per_hour)
                bike.quantity = data.get('quantity', bike.quantity)
                bike.save()
                return JsonResponse({'success': True, 'message': 'Cập nhật xe đạp thành công!'})
            else:
                # Create new bike
                bike = Bike.objects.create(
                    name=data.get('model'),
                    bike_type=data.get('type'),
                    price_per_hour=data.get('price'),
                    quantity=data.get('quantity')
                )
                return JsonResponse({'success': True, 'message': 'Thêm xe đạp thành công!', 'id': bike.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
@csrf_exempt
def dashboard_bike_delete_api(request, bike_id):
    """API xóa bike"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'DELETE':
        try:
            bike = Bike.objects.get(id=bike_id)
            bike.delete()
            return JsonResponse({'success': True, 'message': 'Xóa xe đạp thành công!'})
        except Bike.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Không tìm thấy xe đạp'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
@csrf_exempt
def dashboard_rental_update_status_api(request, rental_id):
    """API cập nhật trạng thái đơn thuê"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_status = data.get('status')
            
            rental = BikeRental.objects.get(id=rental_id)
            rental.status = new_status
            rental.save()
            
            # Gửi thông báo qua WebSocket nếu có đơn mới
            try:
                from channels.layers import get_channel_layer
                from asgiref.sync import async_to_sync
                
                channel_layer = get_channel_layer()
                if channel_layer:
                    async_to_sync(channel_layer.group_send)(
                        'admin_notifications',
                        {
                            'type': 'rental_notification',
                            'message': f'Đơn thuê {rental.rental_code} đã được cập nhật trạng thái: {rental.get_status_display()}'
                        }
                    )
            except Exception as e:
                # Nếu WebSocket không khả dụng, bỏ qua
                pass
            
            return JsonResponse({'success': True, 'message': 'Cập nhật trạng thái thành công!'})
        except BikeRental.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Không tìm thấy đơn thuê'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def dashboard_charts_api(request):
    """API trả về dữ liệu cho biểu đồ"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    now = timezone.now()
    # Dữ liệu 7 ngày gần nhất
    dates = []
    rental_counts = []
    revenue_data = []
    
    for i in range(6, -1, -1):
        date = (now - timedelta(days=i)).date()
        dates.append(date.strftime('%d/%m'))
        
        day_start = timezone.make_aware(datetime.combine(date, datetime.min.time()))
        day_end = timezone.make_aware(datetime.combine(date, datetime.max.time()))
        
        count = BikeRental.objects.filter(
            created_at__gte=day_start,
            created_at__lte=day_end
        ).count()
        rental_counts.append(count)
        
        revenue = BikeRental.objects.filter(
            created_at__gte=day_start,
            created_at__lte=day_end,
            status__in=['completed', 'renting']
        ).aggregate(Sum('total_price'))['total_price__sum'] or 0
        revenue_data.append(float(revenue))
    
    # Thống kê theo loại xe
    bike_type_stats = {}
    for bike_type_code, bike_type_name in BikeRental.BIKE_TYPES:
        count = BikeRental.objects.filter(bike_type=bike_type_code).count()
        bike_type_stats[bike_type_name] = count
    
    return JsonResponse({
        'dates': dates,
        'rental_counts': rental_counts,
        'revenue_data': revenue_data,
        'bike_type_stats': bike_type_stats,
    })

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
    return redirect('home')

# Profile user
@login_required
def profile_view(request):
    """Trang profile của user"""
    user = request.user
    
    if request.method == 'POST':
        # Cập nhật thông tin profile
        if 'full_name' in request.POST:
            user.full_name = request.POST.get('full_name', user.full_name)
            user.phone_number = request.POST.get('phone_number', user.phone_number)
            
            if 'avatar' in request.FILES:
                user.avatar = request.FILES['avatar']
            
            user.save()
            messages.success(request, 'Cập nhật thông tin thành công!')
            return redirect('profile')
        
        # Đổi mật khẩu
        elif 'old_password' in request.POST:
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            if not user.check_password(old_password):
                messages.error(request, 'Mật khẩu hiện tại không đúng!')
            elif new_password != confirm_password:
                messages.error(request, 'Mật khẩu mới và xác nhận không khớp!')
            elif len(new_password) < 8:
                messages.error(request, 'Mật khẩu phải có ít nhất 8 ký tự!')
            else:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Đổi mật khẩu thành công! Vui lòng đăng nhập lại.')
                return redirect('login')
    
    # Lấy danh sách đơn thuê của user
    rentals = BikeRental.objects.filter(
        Q(user=user) | Q(email=user.email)
    ).order_by('-created_at')[:20]
    
    context = {
        'user': user,
        'rentals': rentals,
    }
    return render(request, 'profile.html', context)

# Export báo cáo
@login_required
def export_rentals_report(request):
    """Xuất báo cáo đơn thuê ra Excel/CSV"""
    if not request.user.is_staff:
        messages.error(request, 'Bạn không có quyền truy cập chức năng này.')
        return redirect('home')
    
    from django.http import HttpResponse
    from django.db.models import Sum
    import csv
    from datetime import datetime
    
    format_type = request.GET.get('format', 'csv')  # csv hoặc excel
    
    # Lấy dữ liệu đơn thuê
    rentals = BikeRental.objects.all().order_by('-created_at')
    
    if format_type == 'csv':
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="rentals_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        # Header
        writer.writerow([
            'Mã đơn', 'Họ tên', 'Email', 'Số điện thoại', 'Loại xe', 
            'Số lượng', 'Ngày nhận', 'Ngày trả', 'Trạng thái', 'Tổng tiền', 'Ngày tạo'
        ])
        
        # Data
        for rental in rentals:
            writer.writerow([
                rental.rental_code,
                rental.full_name,
                rental.email,
                rental.phone,
                rental.get_bike_type_display(),
                rental.quantity,
                rental.pickup_date.strftime('%d/%m/%Y'),
                rental.return_date.strftime('%d/%m/%Y'),
                rental.get_status_display(),
                f"{rental.total_price:,.0f}" if rental.total_price else "0",
                rental.created_at.strftime('%d/%m/%Y %H:%M:%S')
            ])
        
        return response
    
    elif format_type == 'excel':
        try:
            import openpyxl
            from openpyxl.styles import Font, Alignment
            
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Báo cáo đơn thuê"
            
            # Header
            headers = [
                'Mã đơn', 'Họ tên', 'Email', 'Số điện thoại', 'Loại xe', 
                'Số lượng', 'Ngày nhận', 'Ngày trả', 'Trạng thái', 'Tổng tiền', 'Ngày tạo'
            ]
            ws.append(headers)
            
            # Style header
            for cell in ws[1]:
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal='center')
            
            # Data
            for rental in rentals:
                ws.append([
                    rental.rental_code,
                    rental.full_name,
                    rental.email,
                    rental.phone,
                    rental.get_bike_type_display(),
                    rental.quantity,
                    rental.pickup_date.strftime('%d/%m/%Y'),
                    rental.return_date.strftime('%d/%m/%Y'),
                    rental.get_status_display(),
                    rental.total_price if rental.total_price else 0,
                    rental.created_at.strftime('%d/%m/%Y %H:%M:%S')
                ])
            
            # Auto adjust column width
            for column in ws.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws.column_dimensions[column_letter].width = adjusted_width
            
            response = HttpResponse(
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename="rentals_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx"'
            
            wb.save(response)
            return response
        except ImportError:
            messages.error(request, 'Cần cài đặt openpyxl để xuất file Excel: pip install openpyxl')
            return redirect('dashboard')
    
    return redirect('dashboard')


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
            
            # Gửi thông báo qua WebSocket cho admin
            try:
                from channels.layers import get_channel_layer
                from asgiref.sync import async_to_sync
                
                channel_layer = get_channel_layer()
                if channel_layer:
                    async_to_sync(channel_layer.group_send)(
                        'admin_notifications',
                        {
                            'type': 'rental_notification',
                            'message': f'Có đơn thuê mới: {rental.rental_code} từ {rental.full_name}'
                        }
                    )
            except Exception as e:
                # Nếu WebSocket không khả dụng, bỏ qua
                pass

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