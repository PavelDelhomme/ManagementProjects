from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name="profile"),
    path('projects/', include(('projects.urls', 'projects'), namespace='projects')),
]
