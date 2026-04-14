from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from bookings.choices import BookingStatusChoices
from bookings.forms import BookingCreateForm, BookingCancelForm
from bookings.models import Booking
from workshops.models import Workshop

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
                self.workshop.status = 'full'

            self.workshop.save()

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

class BookingCancelView(LoginRequiredMixin, UpdateView):
    model = Booking
    form_class = BookingCancelForm
    template_name = 'bookings/booking-cancel.html'
    success_url = reverse_lazy('my-bookings')

    def get_queryset(self):
        return Booking.objects.filter(participant=self.request.user)

    def form_valid(self, form):
        booking = form.instance

        if booking.status != BookingStatusChoices.CANCELLED:
            booking.status = BookingStatusChoices.CANCELLED
            booking.save()

            workshop = booking.workshop
            workshop.available_spots += 1

            if workshop.status == 'full':
                workshop.status = 'upcoming'

            workshop.save()

        messages.success(self.request, 'Booking cancelled successfully.')
        return redirect(self.success_url)