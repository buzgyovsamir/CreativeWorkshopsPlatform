from django.urls import path

from bookings.views import BookingCreateView, MyBookingsListView, BookingCancelView

urlpatterns = [
    path('my-bookings/', MyBookingsListView.as_view(), name='my-bookings'),
    path('create/<int:workshop_pk>/', BookingCreateView.as_view(), name='booking-create'),
    path('<int:pk>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),
]