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
    phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True, default='')
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

# Model quản lý xe đạp
class Bike(models.Model):
    BIKE_TYPES = [
        ('mountain', 'Xe đạp leo núi'),
        ('road', 'Xe đạp đường trường'),
        ('electric', 'Xe đạp điện'),
        ('kids', 'Xe đạp trẻ em'),
        ('assist', 'Xe đạp trợ lực'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Tên mẫu xe")
    bike_type = models.CharField(max_length=20, choices=BIKE_TYPES, verbose_name="Loại xe")
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Giá thuê/giờ (VNĐ)")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Số lượng")
    image = models.ImageField(upload_to='bikes/', blank=True, null=True, verbose_name="Hình ảnh")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.get_bike_type_display()}"

    class Meta:
        verbose_name = "Xe đạp"
        verbose_name_plural = "Danh sách xe đạp"
        ordering = ['-created_at']

#Thuê xe đạp
class BikeRental(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ duyệt'),
        ('approved', 'Đã duyệt'),
        ('rejected', 'Từ chối'),
        ('renting', 'Đang thuê'),
        ('completed', 'Đã hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ]
    
    BIKE_TYPES = [
        ('mountain', 'Xe đạp leo núi'),
        ('road', 'Xe đạp đường trường'),
        ('electric', 'Xe đạp điện'),
        ('kids', 'Xe đạp trẻ em'),
        ('assist', 'Xe đạp trợ lực'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Người thuê")
    bike = models.ForeignKey(Bike, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Xe đạp")
    full_name = models.CharField(max_length=100, verbose_name="Họ tên")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=10, verbose_name="Số điện thoại")
    bike_type = models.CharField(max_length=20, choices=BIKE_TYPES, verbose_name="Loại xe")
    quantity = models.IntegerField(verbose_name="Số lượng")
    pickup_date = models.DateField(verbose_name="Ngày nhận")
    return_date = models.DateField(verbose_name="Ngày trả")
    message = models.TextField(blank=True, verbose_name="Ghi chú")
    rental_code = models.CharField(max_length=8, unique=True, verbose_name="Mã đơn")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    total_price = models.DecimalField(max_digits=12, decimal_places=0, null=True, blank=True, verbose_name="Tổng tiền")

    def save(self, *args, **kwargs):
        if not self.rental_code:
            # Generate random 8-character code
            self.rental_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        # Tính tổng tiền nếu có bike và giá
        if self.bike and self.pickup_date and self.return_date:
            days = (self.return_date - self.pickup_date).days + 1
            hours = days * 24  # Giả sử thuê theo ngày, mỗi ngày 24 giờ
            self.total_price = self.bike.price_per_hour * hours * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.rental_code}"

    class Meta:
        verbose_name = "Đơn thuê xe"
        verbose_name_plural = "Đơn thuê xe"
        ordering = ['-created_at'] 