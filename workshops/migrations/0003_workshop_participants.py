# Generated manually for relationship exposure through existing Booking model.

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
        ('workshops', '0002_seed_categories_and_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshop',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='booked_workshops', through='bookings.Booking', to=settings.AUTH_USER_MODEL),
        ),
    ]
