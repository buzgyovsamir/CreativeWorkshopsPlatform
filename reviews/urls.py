from django.urls import path

from reviews.views import ReviewListView, ReviewCreateView, ReviewUpdateView, ReviewDeleteView

urlpatterns = [
    path('', ReviewListView.as_view(), name='review-list'),
    path('create/<int:workshop_pk>/', ReviewCreateView.as_view(), name='review-create'),
    path('<int:pk>/edit/', ReviewUpdateView.as_view(), name='review-edit'),
    path('<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
]