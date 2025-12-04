# 🚴 Django Web Bike Rental System

[![Django](https://img.shields.io/badge/Django-5.1.4-092E20?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=flat-square)]()

> Hệ thống quản lý cho thuê xe đạp trực tuyến được xây dựng bằng Django Framework với đầy đủ tính năng quản lý, thanh toán, và API cho mobile apps.

---

## 📸 Screenshots

### Homepage
![Homepage](screenshots/homepage.png)
*Trang chủ với banner đẹp mắt và danh sách xe đạp nổi bật*

### Dashboard Admin
![Admin Dashboard](screenshots/admin-dashboard.png)
*Dashboard quản trị với thống kê chi tiết và biểu đồ trực quan*

### Customer Dashboard
![Customer Dashboard](screenshots/customer-dashboard.png)
*Trang quản lý của khách hàng với lịch sử đặt xe và thanh toán*

### Booking Calendar
![Booking Calendar](screenshots/booking-calendar.png)
*Lịch đặt xe trực quan với hiển thị availability real-time*

### Mobile App API
![API Documentation](screenshots/api-docs.png)
*API Documentation với Swagger UI đầy đủ*

---

## ✨ Tính Năng Chính

### 🎯 Core Features
- ✅ **Quản lý Xe Đạp**: CRUD đầy đủ với phân loại, hình ảnh, mô tả chi tiết
- ✅ **Đặt Xe Trực Tuyến**: Form đặt xe với validation và calendar view
- ✅ **Quản lý Đơn Thuê**: Workflow đầy đủ từ pending → approved → renting → completed
- ✅ **Thanh Toán Online**: Tích hợp VNPay, MoMo, ZaloPay với callback handling
- ✅ **Đánh Giá & Review**: Hệ thống rating/review sau khi thuê xe
- ✅ **Thông Báo**: Email, SMS, và In-app notifications với preferences

### 👥 User Management
- ✅ **Authentication**: Login/Register với django-allauth
- ✅ **Social Login**: Đăng nhập bằng Facebook, Google
- ✅ **Profile Management**: Cập nhật thông tin, avatar, đổi mật khẩu
- ✅ **Customer Dashboard**: Xem lịch sử, trạng thái đơn, thanh toán

### 🔍 Advanced Features
- ✅ **Tìm Kiếm & Lọc**: Full-text search, filter theo loại/giá/ngày
- ✅ **Lịch Đặt Xe**: Calendar view với real-time availability
- ✅ **Quản Lý Tồn Kho**: Tự động trừ số lượng, cảnh báo hết hàng
- ✅ **Báo Cáo & Export**: Xuất Excel/CSV/PDF với filters

### 🔐 Security & Performance
- ✅ **Rate Limiting**: Bảo vệ API và forms khỏi spam
- ✅ **CSRF/XSS Protection**: Bảo mật toàn diện
- ✅ **Database Indexing**: Tối ưu query performance
- ✅ **Caching**: Redis caching cho static content
- ✅ **Error Handling**: Custom error pages và logging

### 📱 Mobile API
- ✅ **RESTful API**: Đầy đủ endpoints cho iOS/Android
- ✅ **JWT Authentication**: Secure token-based authentication
- ✅ **API Documentation**: Swagger/OpenAPI docs
- ✅ **Push Notifications**: Support cho mobile apps

### 🌐 Internationalization
- ✅ **Multi-language**: Hỗ trợ Tiếng Việt và Tiếng Anh
- ✅ **i18n Support**: Translation files đầy đủ
- ✅ **Language Switcher**: Chuyển đổi ngôn ngữ dễ dàng

### 📊 Analytics & Monitoring
- ✅ **Google Analytics 4**: Tracking user behavior
- ✅ **Conversion Tracking**: Theo dõi đơn hàng và revenue
- ✅ **Performance Monitoring**: Request time tracking
- ✅ **Error Tracking**: Centralized error logging
- ✅ **Health Checks**: API endpoints cho monitoring

### 💾 Backup & Recovery
- ✅ **Automated Backups**: Daily database backups
- ✅ **Backup Verification**: Kiểm tra integrity
- ✅ **Retention Policy**: Tự động xóa backups cũ
- ✅ **Disaster Recovery**: Management commands

---

## 🛠️ Công Nghệ Sử Dụng

### Backend
- **Django 5.1.4** - Web framework
- **Django REST Framework** - API framework
- **Django Channels** - WebSocket support
- **PostgreSQL/SQLite** - Database
- **Redis** - Caching & message broker

### Frontend
- **HTML5/CSS3** - Responsive design
- **JavaScript/jQuery** - Dynamic interactions
- **Chart.js** - Data visualization
- **Bootstrap** - UI framework

### Authentication & Security
- **django-allauth** - Social authentication
- **JWT** - Token-based auth
- **django-simple-captcha** - CAPTCHA protection
- **Rate Limiting** - Custom middleware

### Payment Integration
- **VNPay** - Payment gateway
- **MoMo** - Payment gateway (placeholder)
- **ZaloPay** - Payment gateway (placeholder)

### Tools & Utilities
- **django-import-export** - Data import/export
- **reportlab** - PDF generation
- **openpyxl** - Excel export
- **coverage** - Test coverage

---

## 📁 Cấu Trúc Project

```
DjangoWebBikeRetal/
├── myproject/
│   ├── app_admin/              # Main application
│   │   ├── models.py           # Database models
│   │   ├── views.py            # View functions
│   │   ├── admin.py            # Django admin
│   │   ├── forms.py            # Form classes
│   │   ├── middleware.py       # Custom middleware
│   │   ├── mobile_api/         # Mobile API endpoints
│   │   ├── management/         # Management commands
│   │   ├── tests/              # Test suite
│   │   └── ...
│   ├── app_home/               # Home app
│   │   ├── templates/          # HTML templates
│   │   ├── static/             # CSS, JS, images
│   │   └── views.py
│   ├── myproject/              # Project settings
│   │   ├── settings.py         # Main settings
│   │   ├── urls.py             # URL routing
│   │   └── ...
│   ├── media/                  # Uploaded files
│   ├── static/                 # Static files
│   ├── logs/                   # Application logs
│   ├── backups/                # Database backups
│   ├── locale/                 # Translation files
│   ├── manage.py
│   └── requirements.txt
├── screenshots/                # Project screenshots
├── docs/                       # Documentation
├── .env.example                # Environment variables template
├── .gitignore
└── README.md                   # This file
```

---

## 🚀 Cài Đặt

### Yêu Cầu Hệ Thống
- Python 3.8+
- Django 5.1+
- PostgreSQL (recommended) hoặc SQLite
- Redis (optional, for caching)

### Bước 1: Clone Repository
```bash
git clone https://github.com/yourusername/django-web-bike-rental.git
cd django-web-bike-rental
```

### Bước 2: Tạo Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Bước 3: Cài Đặt Dependencies
```bash
cd myproject
pip install -r requirements.txt
```

### Bước 4: Cấu Hình Environment Variables
```bash
# Copy file .env.example
cp .env.example .env

# Chỉnh sửa .env với các thông tin của bạn
```

Các biến môi trường quan trọng:
```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/1

# Payment Gateways
VNPAY_TMN_CODE=your-tmn-code
VNPAY_HASH_SECRET=your-hash-secret

# Email Settings
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password

# Google Analytics
GOOGLE_ANALYTICS_ID=your-ga-id
GOOGLE_ANALYTICS_ENABLED=True

# Backup Settings
BACKUP_RETENTION_DAYS=30
```

### Bước 5: Chạy Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Bước 6: Tạo Superuser
```bash
python manage.py createsuperuser
```

### Bước 7: Collect Static Files
```bash
python manage.py collectstatic
```

### Bước 8: Chạy Server
```bash
python manage.py runserver
```

Truy cập: http://localhost:8000

---

## ⚙️ Cấu Hình

### Database
Mặc định sử dụng SQLite. Để chuyển sang PostgreSQL:

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bike_rental',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Redis (Optional)
Cài đặt Redis và cấu hình:
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### Payment Gateways
1. **VNPay**: Đăng ký tài khoản tại [VNPay](https://sandbox.vnpayment.vn/)
2. Lấy TMN Code và Hash Secret
3. Cấu hình trong `.env`

---

## 📖 Sử Dụng

### Quản Trị Viên
1. Đăng nhập vào `/admin/` với superuser account
2. Quản lý xe đạp: Thêm/sửa/xóa, upload hình ảnh
3. Duyệt đơn thuê: Approve/reject từ dashboard
4. Xem báo cáo: Export Excel/CSV/PDF
5. Quản lý users: Xem danh sách, phân quyền

### Khách Hàng
1. Đăng ký/Đăng nhập tài khoản
2. Xem danh sách xe đạp với search/filter
3. Đặt xe: Chọn ngày, số lượng, điền form
4. Thanh toán: VNPay hoặc tiền mặt
5. Đánh giá: Rate và review sau khi thuê
6. Dashboard: Xem lịch sử, cập nhật profile

---

## 📱 API Documentation

### Mobile API Endpoints

#### Authentication
- `POST /mobile-api/auth/register/` - Đăng ký
- `POST /mobile-api/auth/login/` - Đăng nhập
- `POST /mobile-api/auth/refresh/` - Refresh token

#### Bikes
- `GET /mobile-api/bikes/` - Danh sách xe
- `GET /mobile-api/bikes/{id}/` - Chi tiết xe
- `GET /mobile-api/bikes/{id}/availability/` - Kiểm tra availability

#### Rentals
- `GET /mobile-api/rentals/` - Lịch sử đặt xe
- `POST /mobile-api/rentals/` - Tạo đơn thuê
- `POST /mobile-api/rentals/{id}/cancel/` - Hủy đơn

#### Reviews
- `GET /mobile-api/reviews/` - Danh sách reviews
- `POST /mobile-api/reviews/` - Tạo review

#### Payments
- `GET /mobile-api/payments/` - Lịch sử thanh toán
- `POST /mobile-api/payments/create_payment/` - Tạo thanh toán

#### Notifications
- `GET /mobile-api/notifications/` - Danh sách thông báo
- `POST /mobile-api/notifications/{id}/mark_read/` - Đánh dấu đã đọc

### API Documentation UI
Truy cập: http://localhost:8000/api/docs/

![API Docs](screenshots/api-docs.png)

---

## 🧪 Testing

### Chạy Tests
```bash
python manage.py test
```

### Test Coverage
```bash
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Test Files
- `app_admin/tests/test_models.py` - Model tests
- `app_admin/tests/test_views.py` - View tests
- `app_admin/tests/test_api.py` - API tests

---

## 🔄 Backup & Recovery

### Tạo Backup
```bash
python manage.py create_backup --type full --cleanup
```

### Liệt Kê Backups
```bash
python manage.py list_backups
```

### Restore Backup
```bash
python manage.py restore_backup /path/to/backup.sqlite3.gz --confirm
```

### Automated Daily Backup
Thêm vào crontab:
```bash
0 2 * * * cd /path/to/project && python manage.py create_backup --type full --cleanup
```

---

## 📊 Monitoring

### Health Check
```bash
GET /api/health/
```

### Metrics (Staff Only)
```bash
GET /api/metrics/
```

### Logs
Logs được lưu tại: `logs/application.log`

---

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG = False`
- [ ] Cấu hình `ALLOWED_HOSTS`
- [ ] Sử dụng PostgreSQL
- [ ] Setup Redis
- [ ] Cấu hình HTTPS/SSL
- [ ] Setup email backend (SMTP)
- [ ] Cấu hình static files (CDN)
- [ ] Setup automated backups
- [ ] Configure monitoring

### Deploy với Docker
```bash
docker-compose up -d
```

### Deploy với Gunicorn
```bash
gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
```

---

## 📝 Features Checklist

- [x] User Authentication & Authorization
- [x] Bike Management (CRUD)
- [x] Rental Management với Workflow
- [x] Payment Integration (VNPay)
- [x] Review & Rating System
- [x] Notification System (Email/SMS/In-app)
- [x] Search & Filter
- [x] Booking Calendar
- [x] Inventory Management
- [x] Customer Dashboard
- [x] Admin Dashboard với Charts
- [x] RESTful API cho Mobile
- [x] JWT Authentication
- [x] API Documentation (Swagger)
- [x] Multi-language Support (i18n)
- [x] SEO Optimization
- [x] Analytics Tracking (GA4)
- [x] Automated Backups
- [x] Performance Monitoring
- [x] Comprehensive Testing

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- Django Framework team
- Django REST Framework
- All open-source contributors
- Payment gateway providers (VNPay, MoMo, ZaloPay)

---

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/django-web-bike-rental/issues)
- **Email**: support@example.com
- **Documentation**: [Full Documentation](docs/)

---

## 📈 Roadmap

### Version 2.0 (Coming Soon)
- [ ] Mobile Apps (iOS & Android)
- [ ] Real-time chat support
- [ ] Advanced analytics dashboard
- [ ] Multi-store management
- [ ] Subscription plans
- [ ] Referral program
- [ ] Social sharing features

---

<div align="center">

**⭐ Nếu project này hữu ích, hãy Star cho repo nhé! ⭐**

Made with ❤️ using Django

</div>

