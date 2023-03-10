from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Project(models.Model):
    """
    Project model
    """
    name = models.CharField(max_length=200)  # project name
    description = models.TextField()  # project description
    assigned_to = models.ManyToManyField(User, related_name='assigned_projects')  # users assigned to the project
    start_date = models.DateField()  # project start date
    end_date = models.DateField()  # project end date
    comments = models.TextField(blank=True)  # project comments


class Task(models.Model):
    """
    Task model
    """
    name = models.CharField(max_length=200)  # task name
    description = models.TextField()  # task description
    assigned_to = models.ManyToManyField(User, related_name='assigned_tasks')  # users assigned to the task
    # project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  # project to which the task belongs
    start_date = models.DateField()  # task start date
    end_date = models.DateField()  # task end date
    priority = models.IntegerField(default=1)  # task priority
    status = models.CharField(max_length=20, choices=[('incomplete', 'Incomplète'), ('complete', 'Complète')],
                              default='incomplete')  # task status
    comments = models.TextField(blank=True)  # task comments


class Event(models.Model):
    """
    Event model
    """
    title = models.CharField(max_length=200)  # event title
    start_date = models.DateTimeField()  # event start date
    end_date = models.DateTimeField()  # event end date
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  # project to which the event belongs
    task = models.ForeignKey(Task, on_delete=models.CASCADE)  # task to which the event belongs
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # user to which the event belongs
    comments = models.TextField(blank=True)  # event comments
