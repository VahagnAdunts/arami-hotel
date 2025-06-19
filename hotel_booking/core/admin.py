from django.contrib import admin
from .models import Room, Booking, RoomImage, ContactMessage, SeasonalPrice


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'room', 'check_in', 'check_out', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'check_in')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email', 'message')


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1


class SeasonalPriceInline(admin.TabularInline):
    model = SeasonalPrice
    extra = 1


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    inlines = [RoomImageInline, SeasonalPriceInline]
    list_display = ('type', 'price_per_night', 'capacity', 'total_count')


@admin.register(SeasonalPrice)
class SeasonalPriceAdmin(admin.ModelAdmin):
    list_display = ('room', 'start_date', 'end_date', 'price_per_night')
    list_filter = ('start_date', 'end_date')
