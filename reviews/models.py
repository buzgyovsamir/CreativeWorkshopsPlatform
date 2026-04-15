from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from bookings.models import Booking
from bookings.choices import BookingStatusChoices
from workshops.models import Workshop


class Review(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    workshop = models.ForeignKey(
        Workshop,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.TextField()
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'workshop'],
                name='unique_review_per_author_workshop',
            ),
        ]
        ordering = ['-created_at']

    def clean(self):
        if not self.author_id or not self.workshop_id:
            return

        has_valid_booking = Booking.objects.filter(
            participant_id=self.author_id,
            workshop_id=self.workshop_id,
            status=BookingStatusChoices.CONFIRMED,
        ).exists()

        if not has_valid_booking:
            raise ValidationError('You can review only workshops you have booked.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.author} - {self.workshop} ({self.rating})'