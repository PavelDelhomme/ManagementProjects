from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Task


@shared_task
def send_task_notification():
    """
    Send an email to the assigned user of a task if the task is incomplete and the end date is in the past.
    :return:
    """
    tasks = Task.objects.filter(end_date__lt=timezone.now(),
                                status='incomplete')  # récupérer toutes les taches avec la date de fin qui sont déjà dépassée et qui ont le status incomplète
    for task in tasks:  # pour chaque tache
        message = f"La tâche '{task.name}' est en retard. Veuillez la compléter dès que possible."  # message à envoyer
        send_mail(  # envoyer un email
            'Notification de tâche en retard',  # sujet
            message,  # message
            'noreply@projectmanager.com',  # depuis email
            [task.assigned_to.email],  # a email
            fail_silently=False,  # si l'email n'est pas envoyé, afficher une erreur
        )
