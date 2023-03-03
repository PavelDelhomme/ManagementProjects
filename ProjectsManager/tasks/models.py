from django.db import models
from django.contrib.auth import get_user_model
from projects.models import Project

User = get_user_model()


class Task(models.Model):
    """
    Modèle pour la gestion des tâches de projet
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    due_date = models.DateField()
    assigned_users = models.ManyToManyField(User, related_name='assigned_tasks', blank=True)

    def __str__(self):
        return self.name


class TaskFile(models.Model):
    """
    Modèle pour la gestion des fichiers liés à une tâche de projet
    """
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='files')
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='projects/files/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
