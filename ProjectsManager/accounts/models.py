from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Personnalisation du modèle utilisateur Django pour ajouter un champ de statut de gestionnaire
    """
    is_manager = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='users',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
