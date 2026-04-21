from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from bookings.choices import BookingStatusChoices
from bookings.models import Booking
from core.mixins import OrganizerRequiredMixin
from reviews.models import Review
from .forms import WorkshopCreateForm, WorkshopEditForm, WorkshopDeleteForm
from .models import Workshop

class WorkshopListView(ListView):
    model = Workshop
    template_name = 'workshops/workshop-list.html'
    context_object_name = 'workshops'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_published=True)

        city = self.request.GET.get('city')
        if city:
            queryset = queryset.filter(city__icontains=city)

        return queryset.order_by('-created_at')

class WorkshopDetailView(DetailView):
    model = Workshop
    template_name = 'workshops/workshop-detail.html'
    context_object_name = 'workshop'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        workshop = self.object

        context['can_review'] = False
        context['my_review'] = None

        if user.is_authenticated and user != workshop.organizer:
            has_confirmed_booking = Booking.objects.filter(
                participant=user,
                workshop=workshop,
                status=BookingStatusChoices.CONFIRMED,
            ).exists()
            context['my_review'] = Review.objects.filter(author=user, workshop=workshop).first()
            context['can_review'] = has_confirmed_booking and context['my_review'] is None

        return context

class WorkshopCreateView(LoginRequiredMixin, OrganizerRequiredMixin, CreateView):
    model = Workshop
    form_class = WorkshopCreateForm
    template_name = 'workshops/workshop-form.html'
    success_url = reverse_lazy('workshop-list')

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Create Workshop'
        context['button_label'] = 'Create'
        return context


class WorkshopUpdateView(LoginRequiredMixin, OrganizerRequiredMixin, UpdateView):
    model = Workshop
    form_class = WorkshopEditForm
    template_name = 'workshops/workshop-form.html'

    def get_success_url(self):
        return reverse_lazy('workshop-detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return Workshop.objects.filter(organizer=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Edit Workshop'
        context['button_label'] = 'Save Changes'
        return context

class WorkshopDeleteView(LoginRequiredMixin, OrganizerRequiredMixin, DeleteView):
    model = Workshop
    form_class = WorkshopDeleteForm
    template_name = 'workshops/workshop-delete.html'
    success_url = reverse_lazy('workshop-list')

    def get_queryset(self):
        return Workshop.objects.filter(organizer=self.request.user)

class MyWorkshopListView(LoginRequiredMixin, OrganizerRequiredMixin, ListView):
    model = Workshop
    template_name = 'workshops/my-workshops.html'
    context_object_name = 'workshops'

    def get_queryset(self):
        return Workshop.objects.filter(organizer=self.request.user)