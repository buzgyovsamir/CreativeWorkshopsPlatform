from datetime import timedelta

from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from accounts.models import AppUser
from workshops.choices import WorkshopStatusChoices
from workshops.models import Workshop, Category


class WorkshopLogicAndAccessTests(TestCase):
	def setUp(self):
		self.organizers_group, _ = Group.objects.get_or_create(name='Organizers')
		self.participants_group, _ = Group.objects.get_or_create(name='Participants')

		self.organizer = AppUser.objects.create_user(
			username='organizer',
			email='org@example.com',
			password='StrongPass123!',
		)
		self.organizer.groups.add(self.organizers_group)

		self.other_organizer = AppUser.objects.create_user(
			username='organizer2',
			email='org2@example.com',
			password='StrongPass123!',
		)
		self.other_organizer.groups.add(self.organizers_group)

		self.participant = AppUser.objects.create_user(
			username='participant',
			email='participant@example.com',
			password='StrongPass123!',
		)
		self.participant.groups.add(self.participants_group)

		self.category = Category.objects.create(name='Drawing', slug='drawing')

		self.workshop = Workshop.objects.create(
			title='Creative Drawing Basics',
			slug='creative-drawing-basics',
			description='Learn core sketching techniques.',
			start_datetime=timezone.now() + timedelta(days=2),
			end_datetime=timezone.now() + timedelta(days=2, hours=2),
			city='Berlin',
			location='Studio 1',
			price=10,
			capacity=10,
			available_spots=10,
			status=WorkshopStatusChoices.UPCOMING,
			organizer=self.organizer,
			category=self.category,
		)

	def test_workshop_validation_rejects_end_before_start(self):
		workshop = Workshop(
			title='Broken Workshop',
			slug='broken-workshop',
			description='Invalid dates.',
			start_datetime=timezone.now() + timedelta(days=3),
			end_datetime=timezone.now() + timedelta(days=2),
			city='Paris',
			location='Room B',
			price=5,
			capacity=5,
			available_spots=5,
			status=WorkshopStatusChoices.UPCOMING,
			organizer=self.organizer,
			category=self.category,
		)

		with self.assertRaisesMessage(ValidationError, 'End date must be after start date.'):
			workshop.full_clean()

	def test_workshop_create_is_forbidden_for_non_organizer(self):
		self.client.login(username='participant', password='StrongPass123!')
		response = self.client.get(reverse('workshop-create'))
		self.assertEqual(response.status_code, 403)

	def test_workshop_create_page_loads_for_organizer(self):
		self.client.login(username='organizer', password='StrongPass123!')
		response = self.client.get(reverse('workshop-create'))
		self.assertEqual(response.status_code, 200)

	def test_workshop_edit_is_owner_only(self):
		self.client.login(username='organizer2', password='StrongPass123!')
		response = self.client.get(reverse('workshop-edit', kwargs={'pk': self.workshop.pk}))
		self.assertEqual(response.status_code, 404)

	def test_workshop_delete_is_owner_only(self):
		self.client.login(username='organizer2', password='StrongPass123!')
		response = self.client.get(reverse('workshop-delete', kwargs={'pk': self.workshop.pk}))
		self.assertEqual(response.status_code, 404)
