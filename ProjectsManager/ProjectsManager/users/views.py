from django.shortcuts import render
from .forms import CustomUserCreationForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView, login_required


class CustomLoginView(LoginView):
    """
    Vue de connexion personnalisée qui hérite de la classe LoginView.
    La classe LoginView est une classe générique qui permet de gérer la connexion d'un utilisateur.
    Mais elle ne permet pas de personnaliser la page de connexion.
    Donc on crée une classe qui hérite de la classe LoginView et on personnalise la page de connexion.
    Et on utilise cette classe pour gérer la connexion d'un utilisateur.
    :argument LoginView: La classe générique qui permet de gérer la connexion d'un utilisateur.
    """
    template_name = 'login.html'  # On définit le template qui sera utilisé pour la page de connexion
    authentication_form = AuthenticationForm  # On définit le formulaire qui sera utilisé pour la page de connexion
    success_url = reverse_lazy('home')  # On définit l'url de redirection après la connexion


class CustomLogoutView(LogoutView):
    """
    Vue de déconnexion personnalisée qui hérite de la classe LogoutView.
    La classe LogoutView est une classe générique qui permet de gérer la déconnexion d'un utilisateur.
    Mais elle ne permet pas de personnaliser la page de déconnexion.
    Donc on crée une classe qui hérite de la classe LogoutView et on personnalise la page de déconnexion.
    Et on utilise cette classe pour gérer la déconnexion d'un utilisateur.
    :argument LogoutView: La classe générique qui permet de gérer la déconnexion d'un utilisateur.
    """
    next_page = reverse_lazy('login')


class SignUpView(CreateView):
    """
    Vue d'inscription personnalisée qui hérite de la classe CreateView.
    La classe CreateView est une classe générique qui permet de gérer la création d'un objet.
    Mais elle ne permet pas de personnaliser la page d'inscription.
    Donc on crée une classe qui hérite de la classe CreateView et on personnalise la page d'inscription.
    Et on utilise cette classe pour gérer l'inscription d'un utilisateur.
    :argument CreateView: La classe générique qui permet de gérer la création d'un objet.
    """
    form_class = CustomUserCreationForm  # On définit le formulaire qui sera utilisé pour la page d'inscription
    success_url = reverse_lazy('login')  # On définit l'url de redirection après l'inscription
    template_name = 'signup.html'  # On définit le template qui sera utilisé pour la page d'inscription


@login_required
def profile(request):
    return render(request, 'profile.html')
