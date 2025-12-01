from django.contrib import admin
from import_export import resources
from import_export.admin import ExportActionMixin
from django.contrib.auth.admin import UserAdmin

from .models import Store
from .models import Article
from .models import BikeRental
from .models import CustomUser
from .models import Bike




#
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date')
    search_fields = ('title', 'short_description')
    list_filter = ('publish_date',)

#
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone', 'opening_hours', 'order')
    search_fields = ('name', 'address')
    list_editable = ('order',) # Cho phép sửa trực tiếp trường order từ danh sách admin

@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ('name', 'bike_type', 'price_per_hour', 'quantity', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('bike_type', 'is_active', 'created_at')
    list_editable = ('is_active', 'quantity')

@admin.register(BikeRental)
class BikeRentalAdmin(admin.ModelAdmin):
    list_display = ('rental_code', 'full_name', 'email', 'phone', 'bike_type', 'quantity', 'pickup_date', 'return_date', 'status', 'total_price', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'rental_code')
    list_filter = ('bike_type', 'status', 'pickup_date', 'return_date', 'created_at')
    readonly_fields = ('rental_code', 'created_at', 'total_price')
    actions = ['approve_rentals', 'reject_rentals']
    
    def approve_rentals(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f'Đã duyệt {queryset.count()} đơn thuê.')
    approve_rentals.short_description = "Duyệt các đơn đã chọn"
    
    def reject_rentals(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f'Đã từ chối {queryset.count()} đơn thuê.')
    reject_rentals.short_description = "Từ chối các đơn đã chọn"

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'full_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Thông tin cá nhân', {'fields': ('email', 'phone_number', 'full_name')}),
        ('Phân quyền', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Thời gian', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'phone_number', 'full_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('username', 'email', 'phone_number', 'full_name')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)