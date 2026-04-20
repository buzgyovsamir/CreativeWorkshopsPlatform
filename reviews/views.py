from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from core.mixins import ParticipantRequiredMixin
from reviews.forms import ReviewCreateForm, ReviewEditForm, ReviewDeleteForm
from reviews.models import Review
from workshops.models import Workshop

class ReviewListView(ListView):
    model = Review
    template_name = 'reviews/review-list.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        return Review.objects.filter(is_visible=True).select_related('author', 'workshop')

class ReviewCreateView(LoginRequiredMixin, ParticipantRequiredMixin, CreateView):
    model = Review
    form_class = ReviewCreateForm
    template_name = 'reviews/review-create.html'

    def dispatch(self, request, *args, **kwargs):
        self.workshop = get_object_or_404(Workshop, pk=self.kwargs['workshop_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.workshop = self.workshop
        try:
            response = super().form_valid(form)
            messages.success(self.request, 'Review submitted successfully.')
            return response
        except ValidationError as exc:
            for message in exc.messages:
                form.add_error(None, message)
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('workshop-detail', kwargs={'pk': self.workshop.pk})

class ReviewUpdateView(LoginRequiredMixin, ParticipantRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewEditForm
    template_name = 'reviews/review-edit.html'

    def get_queryset(self):
        return Review.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('workshop-detail', kwargs={'pk': self.object.workshop.pk})

class ReviewDeleteView(LoginRequiredMixin, ParticipantRequiredMixin, DeleteView):
    model = Review
    form_class = ReviewDeleteForm
    template_name = 'reviews/review-delete.html'

    def get_queryset(self):
        return Review.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy('workshop-detail', kwargs={'pk': self.object.workshop.pk})