from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

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

class WorkshopCreateView(LoginRequiredMixin, CreateView):
    model = Workshop
    form_class = WorkshopCreateForm
    template_name = 'workshops/workshop-create.html'
    success_url = reverse_lazy('workshop-list')

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)

class WorkshopUpdateView(LoginRequiredMixin, UpdateView):
    model = Workshop
    form_class = WorkshopEditForm
    template_name = 'workshops/workshop-edit.html'

    def get_success_url(self):
        return reverse_lazy('workshop-detail', kwargs={'pk': self.object.pk})

    def get_queryset(self):
        return Workshop.objects.filter(organizer=self.request.user)

class WorkshopDeleteView(LoginRequiredMixin, DeleteView):
    model = Workshop
    form_class = WorkshopDeleteForm
    template_name = 'workshops/workshop-delete.html'
    success_url = reverse_lazy('workshop-list')

    def get_queryset(self):
        return Workshop.objects.filter(organizer=self.request.user)