from django.shortcuts import render
from django.urls import path
from .views import SignUpView, CustomLogoutView, CustomLoginView, profile

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'), # Login page URL (login/)
    path('logout/', CustomLogoutView.as_view(), name='logout'), # Logout page URL (logout/)
    path('signup/', SignUpView.as_view(), name='signup'), # Signup page URL (signup/)
    path('accounts/profile/', profile, name='profile'), # Profile page URL (profile/)
]