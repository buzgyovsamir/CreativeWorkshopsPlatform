from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.models import Group
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from accounts.models import AppUser
from bookings.choices import BookingStatusChoices
from bookings.models import Booking
from workshops.choices import WorkshopStatusChoices
from workshops.models import Workshop, Category


class BookingFlowTests(TestCase):
	def setUp(self):
		self.organizers_group, _ = Group.objects.get_or_create(name='Organizers')
		self.participants_group, _ = Group.objects.get_or_create(name='Participants')

		self.organizer = AppUser.objects.create_user(
			username='organizer',
			email='organizer@example.com',
			password='StrongPass123!',
		)
		self.organizer.groups.add(self.organizers_group)

		self.participant = AppUser.objects.create_user(
			username='participant',
			email='participant@example.com',
			password='StrongPass123!',
		)
		self.participant.groups.add(self.participants_group)

		self.category = Category.objects.create(name='Pottery Test', slug='pottery-test')
		self.workshop = Workshop.objects.create(
			title='Weekend Pottery Basics',
			slug='weekend-pottery-basics',
			description='Create your first pottery pieces.',
			start_datetime=timezone.now() + timedelta(days=1),
			end_datetime=timezone.now() + timedelta(days=1, hours=3),
			city='Sofia',
			location='Studio Clay',
			price=20,
			capacity=2,
			available_spots=2,
			status=WorkshopStatusChoices.UPCOMING,
			organizer=self.organizer,
			category=self.category,
		)

	@patch('bookings.views.send_booking_confirmation_email.delay')
	def test_participant_can_create_booking(self, mocked_delay):
		self.client.login(username='participant', password='StrongPass123!')
		response = self.client.post(
			reverse('booking-create', kwargs={'workshop_pk': self.workshop.pk}),
			data={'notes': 'Looking forward to it!'},
		)

		self.assertRedirects(response, reverse('my-bookings'))
		self.assertTrue(
			Booking.objects.filter(participant=self.participant, workshop=self.workshop).exists()
		)
		self.workshop.refresh_from_db()
		self.assertEqual(self.workshop.available_spots, 1)
		mocked_delay.assert_called_once()

	@patch('bookings.views.send_booking_confirmation_email.delay')
	def test_duplicate_booking_is_blocked(self, mocked_delay):
		Booking.objects.create(participant=self.participant, workshop=self.workshop)
		self.client.login(username='participant', password='StrongPass123!')

		response = self.client.post(
			reverse('booking-create', kwargs={'workshop_pk': self.workshop.pk}),
			data={'notes': 'Second attempt'},
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'already booked')
		self.assertEqual(Booking.objects.filter(participant=self.participant, workshop=self.workshop).count(), 1)
		mocked_delay.assert_not_called()

	@patch('bookings.views.send_booking_confirmation_email.delay')
	def test_self_booking_is_blocked(self, mocked_delay):
		self.organizer.groups.add(self.participants_group)
		self.client.login(username='organizer', password='StrongPass123!')

		response = self.client.post(
			reverse('booking-create', kwargs={'workshop_pk': self.workshop.pk}),
			data={'notes': 'I want to join my own workshop'},
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'cannot book your own workshop')
		self.assertFalse(Booking.objects.filter(participant=self.organizer, workshop=self.workshop).exists())
		mocked_delay.assert_not_called()

	def test_booking_create_forbidden_for_non_participant(self):
		self.client.login(username='organizer', password='StrongPass123!')
		response = self.client.get(reverse('booking-create', kwargs={'workshop_pk': self.workshop.pk}))
		self.assertEqual(response.status_code, 403)

	def test_booking_cancellation_updates_status_and_spots(self):
		booking = Booking.objects.create(participant=self.participant, workshop=self.workshop)
		self.workshop.available_spots = 0
		self.workshop.status = WorkshopStatusChoices.FULL
		self.workshop.save()

		self.client.login(username='participant', password='StrongPass123!')
		response = self.client.post(
			reverse('booking-cancel', kwargs={'pk': booking.pk}),
			data={'confirm': True},
		)

		self.assertRedirects(response, reverse('my-bookings'))
		booking.refresh_from_db()
		self.assertEqual(booking.status, BookingStatusChoices.CANCELLED)
		self.workshop.refresh_from_db()
		self.assertEqual(self.workshop.available_spots, 1)
		self.assertEqual(self.workshop.status, WorkshopStatusChoices.UPCOMING)
