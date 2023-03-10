from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    """
    Un formulaire qui crée un utilisateur, avec aucun privilège, à partir du nom d'utilisateur et du mot de passe donnés.
    """
    class Meta:
        model = get_user_model() # Le modèle utilisateur est défini dans le fichier settings.py
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2') # champs à afficher dans le formulaire