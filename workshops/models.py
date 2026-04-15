from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

from workshops.choices import WorkshopStatusChoices


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(2)],
    )
    slug = models.SlugField(
        unique=True,
    )
    description = models.TextField(
        blank=True,
    )

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(
        max_length=30,
        unique=True,
    )
    slug = models.SlugField(
        unique=True,
    )

    def __str__(self):
        return self.name



class Workshop(models.Model):
    title = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(5)],
    )
    slug = models.SlugField(
        unique=True,
    )
    description = models.TextField()

    image = models.ImageField(
        upload_to='workshop_images/',
        blank=True,
        null=True,
    )

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    city = models.CharField(max_length=50)
    location = models.CharField(max_length=100)

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )

    capacity = models.PositiveIntegerField()
    available_spots = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=WorkshopStatusChoices.choices,
        default=WorkshopStatusChoices.UPCOMING,
    )

    is_published = models.BooleanField(default=True)

    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='workshops',
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='workshops',
    )

    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='workshops',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.start_datetime < timezone.now():
            raise ValidationError('Start date cannot be in the past.')

        if self.end_datetime <= self.start_datetime:
            raise ValidationError('End date must be after start date.')

        if self.available_spots > self.capacity:
            raise ValidationError('Available spots cannot exceed capacity.')

        if self.price < 0:
            raise ValidationError('Price cannot be negative.')

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Workshop.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{counter}'
                counter += 1

            self.slug = slug

        if self.available_spots > self.capacity:
            self.available_spots = self.capacity

        super().save(*args, **kwargs)

    @property
    def is_full(self):
        return self.available_spots <= 0

    @property
    def is_bookable(self):
        return self.is_published and self.status == WorkshopStatusChoices.UPCOMING and self.available_spots > 0

    def __str__(self):
        return self.title