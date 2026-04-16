from rest_framework import generics, permissions

from workshops.models import Workshop
from bookings.models import Booking
from reviews.models import Review

from api.serializers import WorkshopSerializer, BookingSerializer, ReviewSerializer

class WorkshopListAPIView(generics.ListAPIView):
    queryset = Workshop.objects.filter(is_published=True)
    serializer_class = WorkshopSerializer
    permission_classes = [permissions.AllowAny]

class WorkshopDetailAPIView(generics.RetrieveAPIView):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    permission_classes = [permissions.AllowAny]

class MyBookingsAPIView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(
            participant=self.request.user
        ).select_related('workshop')

class ReviewListAPIView(generics.ListAPIView):
    queryset = Review.objects.filter(is_visible=True)
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]