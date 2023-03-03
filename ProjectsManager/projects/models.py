from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Project(models.Model):
    """
    Modèle pour la gestion des projets
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects_managed')
    assigned_users = models.ManyToManyField(User, related_name='assigned_projects', blank=True)
    assigned_groups = models.ManyToManyField('auth.Group', related_name='assigned_projects', blank=True)

    def __str__(self):
        return self.name


class ProjectFile(models.Model):
    """
    Modèle pour la gestion des fichiers liés à un projet
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='files')
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='projects/files/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
