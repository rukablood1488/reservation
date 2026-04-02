from django.contrib import admin
from .models import Location, RoomCategory, CategoryImage, Room, RoomImage, Booking


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('country', 'city', 'address')
    search_fields = ('country', 'city')


class CategoryImageInline(admin.TabularInline):
    model = CategoryImage
    extra = 2
    fields = ('image', 'caption', 'is_main')


@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [CategoryImageInline]


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 3
    fields = ('image', 'caption', 'is_main')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'location', 'capacity', 'price')
    list_filter = ('category', 'location__country', 'location__city')
    search_fields = ('name', 'location__country', 'location__city')
    inlines = [RoomImageInline]


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
