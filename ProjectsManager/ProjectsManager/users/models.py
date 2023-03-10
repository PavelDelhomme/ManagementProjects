from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.

class UserManager(BaseUserManager):
    """
    Un gestionnaire personnalisé pour créer des utilisateurs et des superutilisateurs.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Crée et enregistre un utilisateur avec l'adresse email et le mot de passe donnés.
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        if not email: # Si l'adresse email n'est pas renseignée
            raise ValueError('The Email field is required') # On lève une exception
        email = self.normalize_email(email) # On normalise l'adresse email
        user = self.model(email=email, **extra_fields) # On crée un utilisateur avec l'adresse email et les autres champs
        user.set_password(password) # On définit le mot de passe
        user.save(using=self._db) # On enregistre l'utilisateur
        return user # On retourne l'utilisateur

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Crée et enregistre un superutilisateur avec l'adresse email et le mot de passe donnés.
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        extra_fields.setdefault('is_staff', True) # On définit le champ is_staff à True
        extra_fields.setdefault('is_superuser', True) # On définit le champ is_superuser à True
        return self.create_user(email, password, **extra_fields) # On crée un utilisateur avec l'adresse email et le mot de passe donnés


class User(AbstractUser):
    """
    Un modèle utilisateur personnalisé. Il hérite de la classe AbstractUser.
    """
    phone_number = models.CharField(max_length=20, blank=True, null=True) # Le numéro de téléphone


    email = models.EmailField(max_length=254, unique=True) # L'adresse email
    first_name = models.CharField(max_length=254) # Le prénom
    last_name = models.CharField(max_length=254) # Le nom de famille
    is_active = models.BooleanField(default=True) # Le champ is_active
    is_staff = models.BooleanField(default=False) # Le champ is_staff
    is_superuser = models.BooleanField(default=False) # Le champ is_superuser
    date_joined = models.DateTimeField(auto_now_add=True) # La date d'inscription de l'utilisateur
    last_login = models.DateTimeField(auto_now=True) # La date de la dernière connexion de l'utilisateur

    USERNAME_FIELD = 'email' # Le champ qui sert d'identifiant pour l'utilisateur
    REQUIRED_FIELDS = ['first_name', 'last_name'] # Les champs obligatoires pour l'utilisateur


    groups = models.ManyToManyField( # Les groupes auxquels l'utilisateur appartient
        'auth.Group',  # Le modèle Group
        related_name='user_groups', # Le nom de la relation inverse
        blank=True, # Le champ est facultatif
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', # Le texte d'aide pour le champ
        verbose_name='groups', # Le nom du champ
    )
    user_permissions = models.ManyToManyField( # Les permissions de l'utilisateur
        'auth.Permission', # Le modèle Permission
        related_name='user_permissions', # Le nom de la relation inverse
        blank=True, # Le champ est facultatif
        help_text='Specific permissions for this user.', # Le texte d'aide pour le champ
        verbose_name='user permissions', # Le nom du champ
    )

    objects = UserManager() # Le gestionnaire de l'utilisateur

    def __str__(self):
        return self.email # On retourne l'adresse email de l'utilisateur
