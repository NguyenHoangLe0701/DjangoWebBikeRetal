tải django : pip install django 
update django pip install --upgrade Django

tải các thư viện trong requirements trong terminal :pip install -r requirements.txt
# Ghi lại danh sách thư viện đã cài đặt
pip freeze > requirements.txt 

python  --version
cách kích hoạt môi trường ảo:.\venv\Scripts\activate
*tải django đúng phiên bản
FROM python:3.12-slim
docker pull python:3.12-slim
bật Docker trên máy và dùng lệnh : docker compose up

Chạy PROJECT
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
Login bên thứ 3
pip install django-allauth
tree /f > tree.txt #tạo cây thư mục

#Email
pip install django-templated-mail
pip install python-decouple
# 🚴‍♂️ Dự Án Xedap.vn

## Tính năng nổi bật
- 🚀 **WebSocket**: Gửi thông báo thời gian thực.
- ✅ **Redis**: Lưu cache để tăng hiệu suất.
- ❌ **Google OAuth**: Chưa hoàn thành.

## Lưu ý
💡 Đảm bảo Redis đang chạy trước khi khởi động server.
🔥 Hiệu suất được cải thiện với Django Channels.

Tài Liệu Dự Án Xedap.vn

Tổng Quan

Đây là một ứng dụng web dựa trên Django để quản lý việc bán và cho thuê xe đạp, với bảng điều khiển quản trị (admin dashboard) để quản lý khách hàng, xe đạp, đơn thuê và tạo báo cáo với biểu đồ.

Yêu Cầu Trước

Đảm bảo bạn đã cài đặt những thứ sau trên máy tính của mình:





Python: Phiên bản 3.12 (khuyến nghị)



Docker: Để triển khai container hóa



pip: Trình quản lý gói Python



Virtualenv: Để tạo môi trường Python cô lập

Hướng Dẫn Cài Đặt

1. Cài Đặt Python và Kiểm Tra Phiên Bản

Đảm bảo Python 3.12 được cài đặt trên hệ thống. Kiểm tra phiên bản bằng lệnh:

python --version

Kết quả mong đợi: Python 3.12.x

2. Tạo và Kích Hoạt Môi Trường Ảo
Để cô lập các phụ thuộc, tạo một môi trường ảo:
python -m venv venv
Kích hoạt môi trường ảo:

Trên Windows:

.\venv\Scripts\activate
Trên macOS/Linux:

source venv/bin/activate

3. Cài Đặt Django

Cài đặt Django với phiên bản chính xác (ví dụ: 5.0.7, phiên bản mới nhất tính đến tháng 5/2025):

pip install django==5.0.7

Để cập nhật Django lên phiên bản mới nhất:

pip install --upgrade django

4. Cài Đặt Các Thư Viện Từ requirements.txt

Nếu bạn có file requirements.txt chứa các phụ thuộc của dự án, cài đặt chúng:

pip install -r requirements.txt

Ví dụ file requirements.txt:

django==5.0.7
djangorestframework
django-allauth
django-redis
channels

5. Cấu Hình Docker (Tùy Chọn)

Để chạy dự án trong môi trường container hóa:

Tải Hình Ảnh Python

Sử dụng hình ảnh Python 3.12 slim để triển khai nhẹ:

docker pull python:3.12-slim

Dockerfile

Tạo file Dockerfile cho dự án của bạn:

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

Docker Compose

Tạo file docker-compose.yml:

version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    depends_on:
      - redis

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"

Chạy Docker

Đảm bảo Docker đã được bật trên máy tính của bạn, sau đó khởi động các container:

docker compose up

Lệnh này sẽ khởi động server Django và một instance Redis để lưu cache và hỗ trợ WebSocket.

6. Chạy Dự Án

Nếu không sử dụng Docker, chạy dự án cục bộ:

Áp Dụng Migration

python manage.py makemigrations
python manage.py migrate

Khởi Động Server Phát Triển

python manage.py runserver

Truy cập ứng dụng tại http://localhost:8000.

Tích Hợp Đăng Nhập Bên Thứ Ba

Cài Đặt django-allauth

Để kích hoạt đăng nhập qua Google, Facebook, v.v.:

pip install django-allauth

Cấu Hình





Thêm vào INSTALLED_APPS trong file settings.py:

INSTALLED_APPS = [
    ...
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]
SITE_ID = 1



Thêm URL vào urls.py:

urlpatterns = [
    path('accounts/', include('allauth.urls')),
]



Cấu hình OAuth Google trong settings.py:





# Đăng ký ứng dụng trên Google Developer Console để lấy Client ID và Secret.



## Thêm vào settings.py:

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': 'your-client-id',
            'secret': 'your-secret',
            'key': ''
        }
    }
}



Chạy migration:

python manage.py migrate

Các Thư Viện Nổi Bật Sử Dụng Trong Dự Án

Redis





Mục Đích: Redis được sử dụng để lưu cache và làm broker tin nhắn cho WebSocket.



Cài Đặt:

pip install django-redis



Cấu Hình trong settings.py:

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}



Sử Dụng Trong Dự Án:





Lưu cache dữ liệu bảng điều khiển để tăng hiệu suất.



Ví dụ: Cache view bảng điều khiển trong 15 phút:

from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache 15 phút
def dashboard_view(request):
    return render(request, 'admin_dashboard.html')

WebSocket với Django Channels





Mục Đích: WebSocket được sử dụng để gửi thông báo thời gian thực (ví dụ: thông báo khi có đơn thuê mới).



Cài Đặt:

pip install channels



Cấu Hình:





Thêm vào INSTALLED_APPS trong settings.py:

INSTALLED_APPS = [
    ...
    'channels',
]
ASGI_APPLICATION = 'ten_du_an_cua_ban.asgi.application'



Tạo file routing.py:

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),
]



Tạo file consumers.py:

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))



Cập nhật JavaScript trong bảng điều khiển để kết nối WebSocket:

const ws = new WebSocket('ws://' + window.location.host + '/ws/notifications/');
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    alert('Thông báo: ' + data.message);
};



Sử Dụng Trong Dự Án:





Gửi thông báo thời gian thực cho admin khi có đơn thuê mới được tạo.

Khuyến Nghị Thêm





Bảo Mật: Thêm reCAPTCHA (django-recaptcha) để bảo vệ form đăng nhập.



Hiệu Suất: Sử dụng django-compressor để nén CSS và JavaScript.



Phân Tích: Tích hợp Google Analytics để theo dõi hành vi người dùng.



Email: Cấu hình gửi email thông báo xác nhận đơn thuê bằng hệ thống email của Django.

Xử Lý Sự Cố





Nếu lệnh python manage.py runserver thất bại, đảm bảo tất cả phụ thuộc đã được cài đặt và migration đã được áp dụng.



Đối với vấn đề Docker, kiểm tra xem dịch vụ Redis có đang chạy và các cổng có bị chiếm dụng không.



Nếu WebSocket không hoạt động, xác minh Redis đang chạy và URL WebSocket đúng.

Đóng Góp

Hãy fork kho lưu trữ này, gửi vấn đề hoặc đóng góp qua pull requests.