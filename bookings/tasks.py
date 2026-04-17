from django.conf import settings
from django.core.mail import send_mail

from celery import shared_task


@shared_task
def send_booking_confirmation_email(user_email, workshop_title):
    subject = 'Booking Confirmation'
    message = f'Your booking for "{workshop_title}" was created successfully.'
    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(
        subject,
        message,
        from_email,
        [user_email],
        fail_silently=False,
    )