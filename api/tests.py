from datetime import timedelta

from django.contrib.auth.models import Group
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import AppUser
from bookings.models import Booking
from workshops.choices import WorkshopStatusChoices
from workshops.models import Workshop, Category


class ApiEndpointTests(APITestCase):
	def setUp(self):
		participants_group, _ = Group.objects.get_or_create(name='Participants')

		self.user = AppUser.objects.create_user(
			username='api-user',
			email='api@example.com',
			password='StrongPass123!',
		)
		self.user.groups.add(participants_group)

		self.organizer = AppUser.objects.create_user(
			username='api-organizer',
			email='api-organizer@example.com',
			password='StrongPass123!',
		)

		self.category = Category.objects.create(name='API Category', slug='api-category')
		self.workshop = Workshop.objects.create(
			title='API Workshop Entry',
			slug='api-workshop-entry',
			description='Workshop used for API tests.',
			start_datetime=timezone.now() + timedelta(days=5),
			end_datetime=timezone.now() + timedelta(days=5, hours=2),
			city='Madrid',
			location='Main Hall',
			price=30,
			capacity=12,
			available_spots=12,
			status=WorkshopStatusChoices.UPCOMING,
			organizer=self.organizer,
			category=self.category,
			is_published=True,
		)

		Booking.objects.create(participant=self.user, workshop=self.workshop)

	def test_public_workshop_list_endpoint_is_accessible(self):
		response = self.client.get(reverse('api-workshops'))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertGreaterEqual(len(response.data), 1)

	def test_public_workshop_detail_endpoint_is_accessible(self):
		response = self.client.get(reverse('api-workshop-detail', kwargs={'pk': self.workshop.pk}))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['id'], self.workshop.pk)

	def test_my_bookings_requires_authentication(self):
		response = self.client.get(reverse('api-my-bookings'))
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_authenticated_user_receives_own_bookings(self):
		self.client.login(username='api-user', password='StrongPass123!')
		response = self.client.get(reverse('api-my-bookings'))

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)
		self.assertEqual(response.data[0]['participant'], self.user.username)
