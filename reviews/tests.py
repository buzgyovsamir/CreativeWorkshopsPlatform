from datetime import timedelta

from django.contrib.auth.models import Group
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from accounts.models import AppUser
from bookings.models import Booking
from reviews.models import Review
from workshops.choices import WorkshopStatusChoices
from workshops.models import Workshop, Category


class ReviewPermissionTests(TestCase):
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

		self.other_participant = AppUser.objects.create_user(
			username='participant2',
			email='participant2@example.com',
			password='StrongPass123!',
		)
		self.other_participant.groups.add(self.participants_group)

		self.category = Category.objects.create(name='Photography Test', slug='photography-test-main')
		self.workshop = Workshop.objects.create(
			title='Street Photography Essentials',
			slug='street-photography-essentials',
			description='Practice framing and composition outdoors.',
			start_datetime=timezone.now() + timedelta(days=3),
			end_datetime=timezone.now() + timedelta(days=3, hours=2),
			city='Milan',
			location='Downtown',
			price=15,
			capacity=8,
			available_spots=8,
			status=WorkshopStatusChoices.UPCOMING,
			organizer=self.organizer,
			category=self.category,
		)

	def test_review_create_requires_confirmed_booking(self):
		self.client.login(username='participant', password='StrongPass123!')
		response = self.client.post(
			reverse('review-create', kwargs={'workshop_pk': self.workshop.pk}),
			data={'rating': 5, 'comment': 'Amazing workshop!'},
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'only workshops you have booked')
		self.assertFalse(Review.objects.filter(author=self.participant, workshop=self.workshop).exists())

	def test_review_create_forbidden_for_non_participant(self):
		self.client.login(username='organizer', password='StrongPass123!')
		response = self.client.get(reverse('review-create', kwargs={'workshop_pk': self.workshop.pk}))
		self.assertEqual(response.status_code, 403)

	def test_participant_with_booking_can_create_review(self):
		Booking.objects.create(participant=self.participant, workshop=self.workshop)
		self.client.login(username='participant', password='StrongPass123!')

		response = self.client.post(
			reverse('review-create', kwargs={'workshop_pk': self.workshop.pk}),
			data={'rating': 4, 'comment': 'Very useful session.'},
		)

		self.assertRedirects(response, reverse('workshop-detail', kwargs={'pk': self.workshop.pk}))
		self.assertTrue(Review.objects.filter(author=self.participant, workshop=self.workshop).exists())

	def test_review_edit_is_owner_only(self):
		Booking.objects.create(participant=self.participant, workshop=self.workshop)
		review = Review.objects.create(author=self.participant, workshop=self.workshop, rating=5, comment='Great!')

		self.client.login(username='participant2', password='StrongPass123!')
		response = self.client.get(reverse('review-edit', kwargs={'pk': review.pk}))
		self.assertEqual(response.status_code, 404)

	def test_review_delete_is_owner_only(self):
		Booking.objects.create(participant=self.participant, workshop=self.workshop)
		review = Review.objects.create(author=self.participant, workshop=self.workshop, rating=5, comment='Great!')

		self.client.login(username='participant2', password='StrongPass123!')
		response = self.client.get(reverse('review-delete', kwargs={'pk': review.pk}))
		self.assertEqual(response.status_code, 404)
