from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.db import models


class AppUser(AbstractUser):
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True,
    )
    bio = models.TextField(
        blank=True,
        null=True,
        help_text='Tell others more about yourself.',
    )
    city = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        validators=[MinLengthValidator(2)],
    )

    def __str__(self):
        return self.username