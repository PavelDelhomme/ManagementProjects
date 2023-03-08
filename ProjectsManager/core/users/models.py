from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.FileField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username


class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True, null=True)
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='custom_users',
        help_text='Specific permissions for this user.',
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='custom_users',
        help_text='The groups this user belongs. A user will get all permissions '
                  'granted to each of their groups.',
        related_query_name='custom_user',
    )


class CustomGroup(Group):
    description = models.CharField(max_length=150, blank=True)
    custom_users = models.ManyToManyField(
        CustomUser,
        verbose_name='custom users',
        blank=True,
        related_name='custom_groups',
        help_text='The users that belong to this group.',
        related_query_name='custom_group',
    )


class CustomPermission(Permission):
    description = models.CharField(max_length=150, blank=True)
    custom_users = models.ManyToManyField(
        CustomUser,
        verbose_name='custom users',
        blank=True,
        related_name='custom_permissions',
        help_text='The users that have this permission.',
        related_query_name='custom_permission',
    )
