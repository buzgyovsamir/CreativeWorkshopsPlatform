from django.db import models


class WorkshopStatusChoices(models.TextChoices):
    UPCOMING = 'upcoming', 'Upcoming'
    FULL = 'full', 'Full'
    COMPLETED = 'completed', 'Completed'
    CANCELLED = 'cancelled', 'Cancelled'