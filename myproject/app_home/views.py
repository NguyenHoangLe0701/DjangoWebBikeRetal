from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import BikeRental
from datetime import datetime

def bike_rental(request):
    if request.method == 'POST':
        try:
            # Create new rental record
            rental = BikeRental.objects.create(
                full_name=request.POST.get('full_name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                bike_type=request.POST.get('bike_type'),
                quantity=request.POST.get('quantity'),
                pickup_date=datetime.strptime(request.POST.get('pickup_date'), '%Y-%m-%d').date(),
                return_date=datetime.strptime(request.POST.get('return_date'), '%Y-%m-%d').date(),
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
            send_mail(
                subject=f'Xác nhận đặt xe - Mã số: {rental.rental_code}',
                message=email_plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[rental.email],
                html_message=email_html_message,
                fail_silently=False,
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Đặt xe thành công! Vui lòng kiểm tra email của bạn.',
                'rental_code': rental.rental_code
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return render(request, 'home/bike-rental.html') 