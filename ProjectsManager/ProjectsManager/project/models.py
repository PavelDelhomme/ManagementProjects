import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from django.utils import timezone


def time_remaining(task):
    now = timezone.now()
    remaining = task.end_date - now
    days = remaining.days
    hours, remainder = divmod(remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{days} jours, {hours} heures et {minutes} minutes"


class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Nom'))
    description = models.TextField(verbose_name=_('Description'))

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='created_projects')
    assigned_to = models.ManyToManyField(User, related_name='assigned_projects')
    start_date = models.DateField()
    end_date = models.DateField()
    comments = models.TextField(blank=True)

    def tasks(self):
        return self.task_set.all()

    def can_be_deleted_by(self, user):
        return user.is_superuser or self.created_by == user or user in self.assigned_to.all()


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    assigned_to = models.ManyToManyField(User, related_name='assigned_tasks')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    priority = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=[('incomplete', 'Incomplète'), ('complete', 'Complète')], )
    comments = models.TextField(blank=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_tasks')
    type = models.CharField(max_length=200, default='Tâche')
    avancement = models.IntegerField(default=0)
    temps_estime = models.IntegerField(default=0)
    temps_passe = models.IntegerField(default=0)
    temps_restant = models.IntegerField(default=0)
    date_modification = models.DateTimeField(auto_now=True)
    date_fin_reelle = models.DateTimeField(null=True, blank=True)
    temps_reel = models.IntegerField(null=True, blank=True)
    temps_restant_reel = models.IntegerField(null=True, blank=True)
    temps_estime_reel = models.IntegerField(null=True, blank=True, default=0)
    temps_passe_reel = models.IntegerField(null=True, blank=True)
    avancement_reel = models.IntegerField(null=True, blank=True)
    date_debut_reelle = models.DateTimeField(null=True, blank=True)
    date_debut_prevue = models.DateTimeField(null=True, blank=True)
    date_fin_prevue = models.DateTimeField(null=True, blank=True)
    temps_estime_prevu = models.IntegerField(null=True, blank=True)
    temps_restant_prevu = models.IntegerField(null=True, blank=True)
    temps_passe_prevu = models.IntegerField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('task_detail', kwargs={'project_id': self.project.pk, 'task_id': self.pk})


class Event(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField(blank=True)
