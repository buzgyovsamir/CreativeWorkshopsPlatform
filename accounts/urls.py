from django.urls import path

from .views import RegisterView, AppUserLoginView, AppUserLogoutView, ProfileDetailView, ProfileEditView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', AppUserLoginView.as_view(), name='login'),
    path('logout/', AppUserLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile-details'),
    path('profile/<int:pk>/edit/', ProfileEditView.as_view(), name='profile-edit'),
]