from django.contrib import admin

from bookings.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('participant', 'workshop', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('participant__username', 'workshop__title')
