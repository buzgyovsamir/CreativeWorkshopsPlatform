from django.db import models


class BookingStatusChoices(models.TextChoices):
    CONFIRMED = 'confirmed', 'Confirmed'
    CANCELLED = 'cancelled', 'Cancelled'
    WAITING = 'waiting', 'Waiting'