from django.contrib.auth.models import Group
from django.template import Context, Template
from django.test import RequestFactory, TestCase

from accounts.models import AppUser
from core.views import custom_404, custom_500


class CoreBehaviorTests(TestCase):
	def setUp(self):
		self.factory = RequestFactory()

	def test_custom_404_view_returns_404(self):
		request = self.factory.get('/missing/')
		response = custom_404(request, Exception('Not found'))
		self.assertEqual(response.status_code, 404)

	def test_custom_500_view_returns_500(self):
		request = self.factory.get('/error/')
		response = custom_500(request)
		self.assertEqual(response.status_code, 500)

	def test_is_organizer_template_filter(self):
		organizers_group, _ = Group.objects.get_or_create(name='Organizers')
		user = AppUser.objects.create_user('org-user', password='StrongPass123!')
		user.groups.add(organizers_group)

		rendered = Template('{% load custom_tags %}{{ user|is_organizer }}').render(Context({'user': user}))
		self.assertEqual(rendered, 'True')

	def test_is_participant_template_filter(self):
		participants_group, _ = Group.objects.get_or_create(name='Participants')
		user = AppUser.objects.create_user('participant-user', password='StrongPass123!')
		user.groups.add(participants_group)

		rendered = Template('{% load custom_tags %}{{ user|is_participant }}').render(Context({'user': user}))
		self.assertEqual(rendered, 'True')
