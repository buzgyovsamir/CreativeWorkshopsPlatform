from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class OrganizerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='Organizers').exists()

    def handle_no_permission(self):
        raise PermissionDenied

class ParticipantRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.groups.filter(name='Participants').exists()


class OwnerRequiredMixin(UserPassesTestMixin):
    owner_field = 'organizer'

    def test_func(self):
        obj = self.get_object()
        return getattr(obj, self.owner_field) == self.request.user