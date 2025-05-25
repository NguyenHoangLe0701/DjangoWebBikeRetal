from django.contrib import admin
from import_export import resources
from import_export.admin import ExportActionMixin
from django.contrib.auth.admin import UserAdmin

from .models import Store
from .models import Article
from .models import BikeRental
from .models import CustomUser




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

@admin.register(BikeRental)
class BikeRentalAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'bike_type', 'quantity', 'pickup_date', 'return_date', 'rental_code', 'status')
    search_fields = ('full_name', 'email', 'phone', 'rental_code')
    list_filter = ('bike_type', 'status', 'pickup_date', 'return_date')

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