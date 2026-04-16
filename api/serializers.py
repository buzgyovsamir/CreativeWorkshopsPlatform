from rest_framework import serializers

from workshops.models import Workshop
from bookings.models import Booking
from reviews.models import Review

class WorkshopSerializer(serializers.ModelSerializer):
    organizer = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)

    class Meta:
        model = Workshop
        fields = [
            'id',
            'title',
            'slug',
            'description',
            'city',
            'location',
            'price',
            'available_spots',
            'status',
            'organizer',
            'category',
            'tags',
        ]

class BookingSerializer(serializers.ModelSerializer):
    participant = serializers.StringRelatedField()
    workshop = serializers.StringRelatedField()

    class Meta:
        model = Booking
        fields = [
            'id',
            'participant',
            'workshop',
            'status',
            'created_at',
        ]

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    workshop = serializers.StringRelatedField()

    class Meta:
        model = Review
        fields = [
            'id',
            'author',
            'workshop',
            'rating',
            'comment',
            'created_at',
        ]