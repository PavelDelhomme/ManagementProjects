"""ProjectsManager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from project.views import HomePageView, SignUpView

from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site URL (admin/)
    path('', HomePageView.as_view(), name='home'),  # Home page URL (home/)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),  # Login page URL (login/)
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html', next_page="login"), name='logout'),
    # Logout page URL (logout/)
    path('', include('project.urls')),  # Project app URL (project/)
    path('', include('users.urls')),  # Users app URL (users/)

    # Autres vues de l'application
    # Logout page URL (logout/)
    path('signup/', SignUpView.as_view(), name='signup'),  # Signup page URL (signup/)

    path('', HomePageView.as_view(), name='dashboard'),  # Home page URL (home/)
]
