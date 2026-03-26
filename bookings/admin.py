from django.contrib import admin
from .models import RoomCategory, Room, Booking

@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'capacity', 'price')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'user_name', 'start_time', 'end_time', 'status')
    list_filter = ('status', 'start_time', 'room')
    actions = ['confirm_bookings', 'cancel_bookings']

    def confirm_bookings(self, request, queryset):
        queryset.update(status='confirmed')
    confirm_bookings.short_description = "Підтвердити обрані бронювання"

    def cancel_bookings(self, request, queryset):
        queryset.update(status='cancelled')
    cancel_bookings.short_description = "Скасувати обрані бронювання"