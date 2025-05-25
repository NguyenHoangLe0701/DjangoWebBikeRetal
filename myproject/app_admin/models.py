from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import random
import string


    # Thêm model Article
class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    image = models.ImageField(upload_to='articles/', verbose_name="Hình ảnh") # Cần cài đặt Pillow (pip install Pillow)
    publish_date = models.DateField(verbose_name="Ngày đăng")
    short_description = models.TextField(max_length=300, verbose_name="Mô tả ngắn") # Tóm tắt ngắn gọn
    content = models.TextField(verbose_name="Nội dung chi tiết", blank=True, null=True) # Nội dung đầy đủ bài viết (tùy chọn)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish_date'] # Sắp xếp theo ngày mới nhất trước
        verbose_name = "Bài viết"
        verbose_name_plural = "Bài viết"

#Model Store
class Store(models.Model):
    name = models.CharField(max_length=200, verbose_name="Tên cửa hàng")
    address = models.TextField(verbose_name="Địa chỉ")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Số điện thoại")
    opening_hours = models.CharField(max_length=100, blank=True, null=True, verbose_name="Giờ mở cửa")
    image = models.ImageField(upload_to='Store/', verbose_name="Hình ảnh", null=True, blank=True) # Ảnh sẽ được lưu vào MEDIA_ROOT/store_images/
    order = models.PositiveIntegerField(default=0, verbose_name="Thứ tự hiển thị") # Thêm trường này để dễ sắp xếp

    class Meta:
        verbose_name = "Cửa hàng"
        verbose_name_plural = "Danh sách cửa hàng"
        ordering = ['order', 'name'] # Sắp xếp theo thứ tự và tên

    def __str__(self):
        return self.name
    
#
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    full_name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Người dùng"
        verbose_name_plural = "Người dùng"

#
#
class TrafficReport(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.text} ({self.created_at})"    

#Thuê xe đạp
class BikeRental(models.Model):
    BIKE_TYPES = [
        ('mountain', 'Xe đạp leo núi'),
        ('road', 'Xe đạp đường trường'),
        ('electric', 'Xe đạp điện'),
        ('kids', 'Xe đạp trẻ em'),
        ('assist', 'Xe đạp trợ lực'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    bike_type = models.CharField(max_length=20, choices=BIKE_TYPES)
    quantity = models.IntegerField()
    pickup_date = models.DateField()
    return_date = models.DateField()
    message = models.TextField(blank=True)
    rental_code = models.CharField(max_length=8, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    def save(self, *args, **kwargs):
        if not self.rental_code:
            # Generate random 8-character code
            self.rental_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.rental_code}"

    class Meta:
        verbose_name = "Đơn thuê xe"
        verbose_name_plural = "Đơn thuê xe" 