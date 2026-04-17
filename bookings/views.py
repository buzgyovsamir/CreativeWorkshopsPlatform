from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, FormView, TemplateView

from bookings.choices import BookingStatusChoices
from bookings.forms import BookingCreateForm, BookingCancelForm
from bookings.models import Booking
from workshops.choices import WorkshopStatusChoices
from workshops.models import Workshop

from bookings.tasks import send_booking_confirmation_email

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingCreateForm
    template_name = 'bookings/booking-create.html'

    def dispatch(self, request, *args, **kwargs):
        self.workshop = get_object_or_404(Workshop, pk=self.kwargs['workshop_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.participant = self.request.user
        form.instance.workshop = self.workshop

        try:
            response = super().form_valid(form)
            self.workshop.available_spots -= 1

            if self.workshop.available_spots <= 0:
                self.workshop.status = WorkshopStatusChoices.FULL

            self.workshop.save()

            send_booking_confirmation_email.delay(
                self.request.user.email,
                self.workshop.title,
            )

            messages.success(self.request, 'Booking created successfully.')
            return response

        except IntegrityError:
            form.add_error(None, 'You have already booked this workshop.')
            return self.form_invalid(form)

        except Exception as exc:
            form.add_error(None, str(exc))
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('my-bookings')

class MyBookingsListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/my-bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(participant=self.request.user).select_related('workshop')

class BookingCancelView(LoginRequiredMixin, FormView):
    form_class = BookingCancelForm
    template_name = 'bookings/booking-cancel.html'
    success_url = reverse_lazy('my-bookings')

    def dispatch(self, request, *args, **kwargs):
        self.booking = get_object_or_404(
            Booking.objects.select_related('workshop', 'participant'),
            pk=self.kwargs['pk'],
            participant=request.user,
        )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking'] = self.booking
        return context

    def form_valid(self, form):
        if self.booking.status != BookingStatusChoices.CANCELLED:
            self.booking.status = BookingStatusChoices.CANCELLED
            self.booking.save()

            workshop = self.booking.workshop
            workshop.available_spots += 1

            if workshop.status == WorkshopStatusChoices.FULL:
                workshop.status = WorkshopStatusChoices.UPCOMING

            workshop.save()

        messages.success(self.request, 'Booking cancelled successfully.')
        return redirect(self.success_url)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['my_workshops'] = user.workshops.all()[:5]
        context['my_bookings'] = user.bookings.select_related('workshop')[:5]
        context['my_reviews'] = user.reviews.select_related('workshop')[:5]
        context['is_organizer'] = user.groups.filter(name='Organizers').exists()
        return context