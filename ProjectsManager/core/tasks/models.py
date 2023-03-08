from django.db import models
from projects.models import Project
from users.models import UserProfile


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()

    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ManyToManyField('auth.User', blank=True)
    start_date = models.DateField()
    due_date = models.DateField()
    completed_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
