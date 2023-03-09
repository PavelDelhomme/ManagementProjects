from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Task

@shared_task
def send_task_notification():
    tasks = Task.objects.filter(end_date__lt=timezone.now(), status='incomplete')
    for task in tasks:
        message = f"La tâche '{task.name}' est en retard. Veuillez la compléter dès que possible."
        send_mail(
            'Notification de tâche en retard',
            message,
            'noreply@projectmanager.com',
            [task.assigned_to.email],
            fail_silently=False,
        )
