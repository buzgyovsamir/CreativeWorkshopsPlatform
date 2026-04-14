from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from bookings.choices import BookingStatusChoices
from workshops.models import Workshop


class Booking(models.Model):
    participant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    workshop = models.ForeignKey(
        Workshop,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    status = models.CharField(
        max_length=20,
        choices=BookingStatusChoices.choices,
        default=BookingStatusChoices.CONFIRMED,
    )
    notes = models.TextField(
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['participant', 'workshop'],
                name='unique_booking_per_participant_workshop',
            ),
        ]
        ordering = ['-created_at']

    def clean(self):
        if self.workshop.organizer == self.participant:
            raise ValidationError('You cannot book your own workshop.')

        if self.workshop.available_spots <= 0:
            raise ValidationError('No available spots left for this workshop.')

        if not self.workshop.is_bookable:
            raise ValidationError('This workshop is not available for booking.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.participant} -> {self.workshop}'