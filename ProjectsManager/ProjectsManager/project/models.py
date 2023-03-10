from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class Project(models.Model):
    """
    Project model
    """
    name = models.CharField(max_length=200, verbose_name=_('Nom'))  # project name
    description = models.TextField(verbose_name=_('Description'))  # project description

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='created_projects')
    assigned_to = models.ManyToManyField(User, related_name='assigned_projects')  # users assigned to the project
    start_date = models.DateField()  # project start date
    end_date = models.DateField()  # project end date
    comments = models.TextField(blank=True)  # project comments

    def tasks(self):
        return self.task_set.all()

    def can_be_deleted_by(self, user):
        return user.is_superuser or self.created_by == user or user in self.assigned_to.all()


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

    def get_absolute_url(self):
        return reverse('task_detail', kwargs={'project_id': self.project.pk, 'task_id': self.pk})

    # def get_absolute_url(self):
    #    return reverse('task_update', kwargs={'task_id': self.pk})

    # def get_absolute_url(self):
    # return reverse('task-detail', kwargs={'pk': self.pk})
    # return reverse('task_detail', kwargs={'priject_id': self.project.pk, 'task_id': self.pk})


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


class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    last_message = models.ForeignKey(
        'Message',
        on_delete=models.SET_NULL,
        related_name='conversation_last_messages',
        blank=True,
        null=True,
    )


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
