from django.urls import path

from .views import (
    WorkshopListView,
    WorkshopDetailView,
    WorkshopCreateView,
    WorkshopUpdateView,
    WorkshopDeleteView,
)

urlpatterns = [
    path('', WorkshopListView.as_view(), name='workshop-list'),
    path('create/', WorkshopCreateView.as_view(), name='workshop-create'),
    path('<int:pk>/', WorkshopDetailView.as_view(), name='workshop-detail'),
    path('<int:pk>/edit/', WorkshopUpdateView.as_view(), name='workshop-edit'),
    path('<int:pk>/delete/', WorkshopDeleteView.as_view(), name='workshop-delete'),
]