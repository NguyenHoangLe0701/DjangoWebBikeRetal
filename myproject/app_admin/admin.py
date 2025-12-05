from django.contrib import admin
from import_export import resources
from import_export.admin import ExportActionMixin
from django.contrib.auth.admin import UserAdmin

from .models import Store, Article, BikeRental, CustomUser, Bike, BikeReview, AuditLog, Notification, NotificationPreference, Payment
from django.contrib.admin import DateFieldListFilter
from django.utils.html import format_html




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
    list_display = ('name', 'bike_type', 'price_per_hour', 'quantity', 'get_stock_status', 'is_active', 'get_average_rating', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('bike_type', 'is_active', 'created_at')
    list_editable = ('is_active', 'quantity')
    
    def get_average_rating(self, obj):
        return obj.get_average_rating()
    get_average_rating.short_description = 'Đánh giá TB'
    
    def get_stock_status(self, obj):
        if obj.is_out_of_stock():
            return '❌ Hết hàng'
        elif obj.is_low_stock():
            return '⚠️ Sắp hết'
        else:
            return '✅ Còn hàng'
    get_stock_status.short_description = 'Trạng thái'

@admin.register(BikeReview)
class BikeReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'bike', 'rating', 'title', 'is_verified', 'is_approved', 'created_at')
    search_fields = ('user__username', 'user__email', 'bike__name', 'title', 'comment')
    list_filter = ('rating', 'is_verified', 'is_approved', 'created_at')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('user', 'bike', 'rental')

@admin.register(BikeRental)
class BikeRentalAdmin(admin.ModelAdmin):
    list_display = ('rental_code', 'full_name', 'email', 'phone', 'bike_type', 'quantity', 'pickup_date', 'return_date', 'status', 'total_price', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'rental_code')
    list_filter = (
        'bike_type', 
        'status', 
        ('pickup_date', DateFieldListFilter),
        ('return_date', DateFieldListFilter),
        ('created_at', DateFieldListFilter),
    )
    readonly_fields = ('rental_code', 'created_at', 'total_price')
    date_hierarchy = 'created_at'
    list_per_page = 50
    actions = ['approve_rentals', 'reject_rentals', 'complete_rentals', 'cancel_rentals', 'export_selected_csv']
    
    def approve_rentals(self, request, queryset):
        count = queryset.filter(status='pending').update(status='approved')
        self.message_user(request, f'Đã duyệt {count} đơn thuê.')
    approve_rentals.short_description = "Duyệt các đơn đã chọn"
    
    def reject_rentals(self, request, queryset):
        count = queryset.filter(status__in=['pending', 'approved']).update(status='rejected')
        self.message_user(request, f'Đã từ chối {count} đơn thuê.')
    reject_rentals.short_description = "Từ chối các đơn đã chọn"
    
    def complete_rentals(self, request, queryset):
        count = queryset.filter(status__in=['approved', 'renting']).update(status='completed')
        self.message_user(request, f'Đã hoàn thành {count} đơn thuê.')
    complete_rentals.short_description = "Hoàn thành các đơn đã chọn"
    
    def cancel_rentals(self, request, queryset):
        count = queryset.filter(status__in=['pending', 'approved']).update(status='cancelled')
        self.message_user(request, f'Đã hủy {count} đơn thuê.')
    cancel_rentals.short_description = "Hủy các đơn đã chọn"
    
    def export_selected_csv(self, request, queryset):
        from django.http import HttpResponse
        import csv
        from datetime import datetime
        
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename="rentals_selected_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Mã đơn', 'Họ tên', 'Email', 'Số điện thoại', 'Loại xe', 
            'Số lượng', 'Ngày nhận', 'Ngày trả', 'Trạng thái', 'Tổng tiền', 'Ngày tạo'
        ])
        
        for rental in queryset:
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
    export_selected_csv.short_description = "Xuất CSV các đơn đã chọn"

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

@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'email_enabled', 'sms_enabled', 'push_enabled', 'updated_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('email_enabled', 'sms_enabled', 'push_enabled')
    readonly_fields = ('updated_at',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'title', 'is_read', 'created_at')
    search_fields = ('user__username', 'user__email', 'title', 'message')
    list_filter = ('notification_type', 'is_read', ('created_at', DateFieldListFilter))
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 50
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f'Đã đánh dấu {queryset.count()} thông báo là đã đọc.')
    mark_as_read.short_description = "Đánh dấu đã đọc"
    
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
        self.message_user(request, f'Đã đánh dấu {queryset.count()} thông báo là chưa đọc.')
    mark_as_unread.short_description = "Đánh dấu chưa đọc"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'rental', 'user', 'amount', 'payment_method', 'status', 'created_at', 'paid_at')
    search_fields = ('transaction_id', 'rental__rental_code', 'user__email', 'user__username', 'gateway_transaction_id')
    list_filter = ('payment_method', 'status', ('created_at', DateFieldListFilter))
    readonly_fields = ('transaction_id', 'created_at', 'updated_at', 'paid_at', 'gateway_response', 'ip_address')
    date_hierarchy = 'created_at'
    list_per_page = 50
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('rental', 'user', 'amount', 'payment_method', 'status')
        }),
        ('Giao dịch', {
            'fields': ('transaction_id', 'gateway_transaction_id', 'gateway_response')
        }),
        ('Thông tin khác', {
            'fields': ('ip_address', 'created_at', 'updated_at', 'paid_at')
        }),
    )

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'model_name', 'object_repr', 'user', 'ip_address', 'created_at')
    search_fields = ('model_name', 'object_repr', 'user__username', 'user__email')
    list_filter = ('action', 'model_name', ('created_at', DateFieldListFilter))
    readonly_fields = ('user', 'action', 'model_name', 'object_id', 'object_repr', 'changes', 'ip_address', 'user_agent', 'created_at')
    date_hierarchy = 'created_at'
    list_per_page = 50
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser