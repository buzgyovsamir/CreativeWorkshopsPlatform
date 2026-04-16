from django.urls import path

from api.views import (
    WorkshopListAPIView,
    WorkshopDetailAPIView,
    MyBookingsAPIView,
    ReviewListAPIView,
)

urlpatterns = [
    path('workshops/', WorkshopListAPIView.as_view(), name='api-workshops'),
    path('workshops/<int:pk>/', WorkshopDetailAPIView.as_view(), name='api-workshop-detail'),
    path('bookings/', MyBookingsAPIView.as_view(), name='api-my-bookings'),
    path('reviews/', ReviewListAPIView.as_view(), name='api-reviews'),
]