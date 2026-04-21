from django.contrib.auth.models import Group
from django.urls import reverse
from django.test import TestCase

from accounts.models import AppUser


class AccountsViewsTests(TestCase):
	def setUp(self):
		Group.objects.get_or_create(name='Participants')
		self.user = AppUser.objects.create_user(
			username='john',
			email='john@example.com',
			password='StrongPass123!',
		)

	def test_register_creates_user_and_assigns_participant_group(self):
		response = self.client.post(
			reverse('register'),
			data={
				'username': 'newuser',
				'email': 'new@example.com',
				'password1': 'StrongPass123!',
				'password2': 'StrongPass123!',
			},
		)

		self.assertRedirects(response, reverse('home'))
		created_user = AppUser.objects.get(username='newuser')
		self.assertTrue(created_user.groups.filter(name='Participants').exists())

	def test_login_success(self):
		response = self.client.post(
			reverse('login'),
			data={
				'username': 'john',
				'password': 'StrongPass123!',
			},
		)
		self.assertRedirects(response, reverse('home'))

	def test_profile_detail_requires_authentication(self):
		response = self.client.get(reverse('profile-details', kwargs={'pk': self.user.pk}))
		self.assertEqual(response.status_code, 302)
		self.assertIn(reverse('login'), response.url)

	def test_profile_detail_blocks_access_to_other_user(self):
		other = AppUser.objects.create_user(
			username='other',
			email='other@example.com',
			password='StrongPass123!',
		)
		self.client.login(username='john', password='StrongPass123!')

		response = self.client.get(reverse('profile-details', kwargs={'pk': other.pk}))
		self.assertEqual(response.status_code, 404)

	def test_profile_edit_blocks_access_to_other_user(self):
		other = AppUser.objects.create_user(
			username='other2',
			email='other2@example.com',
			password='StrongPass123!',
		)
		self.client.login(username='john', password='StrongPass123!')

		response = self.client.get(reverse('profile-edit', kwargs={'pk': other.pk}))
		self.assertEqual(response.status_code, 404)
