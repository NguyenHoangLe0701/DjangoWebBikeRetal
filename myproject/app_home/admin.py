from django.contrib import admin
from .models import BikeRental

@admin.register(BikeRental)
class BikeRentalAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone', 'bike_type', 'quantity', 'pickup_date', 'return_date', 'rental_code', 'status', 'created_at')
    list_filter = ('bike_type', 'status', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'rental_code')
    readonly_fields = ('rental_code', 'created_at')
    ordering = ('-created_at',) 