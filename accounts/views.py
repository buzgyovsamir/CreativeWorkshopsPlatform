from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from .forms import AppUserRegisterForm, AppUserLoginForm, ProfileEditForm
from .models import AppUser


class RegisterView(CreateView):
    model = AppUser
    form_class = AppUserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        participants_group = Group.objects.filter(name='Participants').first()
        if participants_group:
            self.object.groups.add(participants_group)
        login(self.request, self.object)
        return response


class AppUserLoginView(LoginView):
    authentication_form = AppUserLoginForm
    template_name = 'registration/login.html'


class AppUserLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = AppUser
    template_name = 'accounts/profile-details.html'
    context_object_name = 'profile'

    def get_queryset(self):
        return AppUser.objects.filter(pk=self.request.user.pk)


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = AppUser
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit.html'

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return AppUser.objects.filter(pk=self.request.user.pk)