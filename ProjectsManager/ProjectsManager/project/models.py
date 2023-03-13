import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from django.utils import timezone


def time_remaining(task):
    """
    Retourne une chaîne représentant le temps restant pour une tâche
    :param task:
    :return:
    """
    now = timezone.now() #  Récupère la date actuelle
    remaining = task.end_date - now # Récupère la différence entre la date de fin et la date actuelle
    days = remaining.days # Récupère le nombre de jours restants
    hours, remainder = divmod(remaining.seconds, 3600) # Récupère le nombre d'heures restantes
    minutes, seconds = divmod(remainder, 60) # Récupère le nombre de minutes restantes
    return f"{days} jours, {hours} heures et {minutes} minutes" # Retourne la chaîne


class Project(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Nom')) # Nom du projet (obligatoire)
    description = models.TextField(verbose_name=_('Description')) # Description du projet (obligatoire)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='created_projects') # Créateur du projet (obligatoire) (un utilisateur peut créer plusieurs projets)
    assigned_to = models.ManyToManyField(User, related_name='assigned_projects') # Utilisateurs assignés au projet (obligatoire) (un utilisateur peut être assigné à plusieurs projets)
    start_date = models.DateField() # Date de début du projet (obligatoire)
    end_date = models.DateField() # Date de fin du projet (optionnel)
    comments = models.TextField(blank=True) # Commentaires sur le projet (optionnel)

    def tasks(self):
        return self.task_set.all() # Récupère toutes les tâches du projet

    def can_be_deleted_by(self, user):
        return user.is_superuser or self.created_by == user or user in self.assigned_to.all() # Vérifie si l'utilisateur peut supprimer le projet

    def __str__(self):
        return self.name # Retourne le nom du projet


class Task(models.Model):
    PRIORITY_CHOICES = ( # Choix de priorité
        (1, _('Faible')),
        (2, _('Moyenne')),
        (3, _('Haute')),
        (4, _('Urgente')),
        (5, _('Critique')),
    )
    name = models.CharField(max_length=200) # Nom de la tâche (obligatoire)
    description = models.TextField() # Description de la tâche (obligatoire)
    assigned_to = models.ManyToManyField(User, related_name='assigned_tasks') # Utilisateurs assignés à la tâche (obligatoire) (un utilisateur peut être assigné à plusieurs tâches)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks') # Projet auquel la tâche est assignée (obligatoire) (un projet peut avoir plusieurs tâches)
    start_date = models.DateField() # Date de début de la tâche (obligatoire)
    end_date = models.DateField(null=True, blank=True) # Date de fin de la tâche (optionnel)
    due_date = models.DateField(null=True, blank=True) # Date d'échéance de la tâche (optionnel)
    priority = models.IntegerField(max_length=len(PRIORITY_CHOICES), choices=PRIORITY_CHOICES, default=1) # Priorité de la tâche (obligatoire)
    status = models.CharField(max_length=20, choices=[('incomplete', 'Incomplète'), ('complete', 'Complète')], ) # Statut de la tâche (obligatoire)
    comments = models.TextField(blank=True) # Commentaires sur la tâche (optionnel)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_tasks') # Créateur de la tâche (obligatoire) (un utilisateur peut créer plusieurs tâches)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_tasks') # Dernier utilisateur à avoir modifié la tâche (obligatoire) (un utilisateur peut modifier plusieurs tâches)
    type = models.CharField(max_length=200, default='Tâche') # Type de la tâche (obligatoire)
    avancement = models.IntegerField(default=0) # Avancement de la tâche (obligatoire)
    temps_estime = models.IntegerField(default=0) # Temps estimé pour la tâche (obligatoire)
    temps_passe = models.IntegerField(default=0) # Temps passé sur la tâche (obligatoire)
    temps_restant = models.IntegerField(default=0) # Temps restant pour la tâche (obligatoire)
    date_modification = models.DateTimeField(auto_now=True) # Date de dernière modification de la tâche (obligatoire)
    date_fin_reelle = models.DateTimeField(null=True, blank=True) # Date de fin réelle de la tâche (optionnel)
    temps_reel = models.IntegerField(null=True, blank=True) # Temps réel passé sur la tâche (optionnel)
    temps_restant_reel = models.IntegerField(null=True, blank=True) # Temps restant réel pour la tâche (optionnel)
    temps_estime_reel = models.IntegerField(null=True, blank=True, default=0) # Temps estimé réel pour la tâche (optionnel)
    temps_passe_reel = models.IntegerField(null=True, blank=True) # Temps passé réel sur la tâche (optionnel)
    avancement_reel = models.IntegerField(null=True, blank=True)  # Avancement réel de la tâche (optionnel)
    date_debut_reelle = models.DateTimeField(null=True, blank=True) # Date de début réelle de la tâche (optionnel)
    date_debut_prevue = models.DateTimeField(null=True, blank=True) # Date de début prévue de la tâche (optionnel)
    temps_estime_prevu = models.IntegerField(null=True, blank=True) # Temps estimé prévu pour la tâche (optionnel)
    date_fin_prevue = models.DateTimeField(null=True, blank=True) # Date de fin prévue de la tâche (optionnel)
    updated_at = models.DateTimeField(auto_now=True) # Date de dernière modification de la tâche (obligatoire)
    priority = models.IntegerField(default=0) # Priorité de la tâche (obligatoire)
    temps_restant_prevu = models.IntegerField(null=True, blank=True) # Temps restant prévu pour la tâche (optionnel)
    temps_passe_prevu = models.IntegerField(null=True, blank=True) # Temps passé prévu sur la tâche (optionnel)
    temps_aujourdhui = models.IntegerField(null=True, blank=True) # Temps passé aujourd'hui sur la tâche (optionnel)

    @property # Propriété qui retourne le temps restant pour la tâche
    def time_remaining(self):
        if self.status == 'complete': # Si la tâche est complète, on retourne 'Tâche terminée'
            return 'Tâche terminée'
        elif self.end_date: # Si la tâche a une date de fin, on retourne le temps restant
            time_left = self.end_date - timezone.now().date() # On calcule le temps restant
            if time_left.days > 0: # Si le temps restant est supérieur à 0, on retourne le temps restant
                return f'{time_left.days} jours restant'
            else:
                return "Aujourd'hui est la date limite"
        else: # Si la tâche n'a pas de date de fin, on retourne 'Pas de date limite'
            return 'Pas de date limite'

    def get_absolute_url(self): # Méthode qui retourne l'url de la tâche (pour la redirection)
        return reverse('task_detail', kwargs={'project_id': self.project.pk, 'task_id': self.pk})

    def save(self, *args, **kwargs): # Méthode qui permet de sauvegarder la tâche
        def save(self, *args, **kwargs):
            if self.pk: # Si la tâche existe déjà
                old_task = Task.objects.get(pk=self.pk) # On récupère l'ancienne tâche
                if old_task.temps_passe_reel is not None: # Si le temps passé réel de l'ancienne tâche est différent de None
                    self.temps_passe_reel = old_task.temps_passe_reel + (self.temps_passe - old_task.temps_passe) # On calcule le temps passé réel
                else: # Sinon
                    self.temps_passe_reel = self.temps_passe - old_task.temps_passe # On calcule le temps passé réel
                if old_task.end_date != self.end_date or old_task.temps_passe != self.temps_passe: # Si la date de fin ou le temps passé a changé
                    if old_task.temps_passe_reel is not None: # Si le temps passé réel de l'ancienne tâche est différent de None
                        self.temps_passe_reel = old_task.temps_passe_reel + (self.temps_passe - old_task.temps_passe) # On calcule le temps passé réel
                    else: # Sinon
                        self.temps_passe_reel = self.temps_passe - old_task.temps_passe # On calcule le temps passé réel
                    self.temps_restant_reel = old_task.temps_estime_reel - self.temps_passe_reel # On calcule le temps restant réel
                    if self.temps_estime_reel > 0: # Si le temps estimé réel est supérieur à 0
                        self.avancement_reel = round(self.temps_passe_reel / self.temps_estime_reel * 100) # On calcule l'avancement réel
                    else: # Sinon
                        self.avancement_reel = 0 # On calcule l'avancement réel
                    if self.temps_passe_reel is not None: # Si le temps passé réel est différent de None
                        self.date_fin_reelle = self.date_debut_reelle + datetime.timedelta(days=self.temps_passe_reel) # On calcule la date de fin réelle
                    else: # Sinon
                        self.date_fin_reelle = None # Retourne la date de fin réelle à None
                else:
                    self.temps_passe_reel = None # Retourne le temps passé réel à None
                    self.temps_restant_reel = None # Retourne le temps restant réel à None
                    self.avancement_reel = None # ...
                    self.date_fin_reelle = None # ...
            else:
                self.date_debut_reelle = timezone.now() # On définit la date de début réelle à la date actuelle
                self.date_debut_prevue = timezone.now() # On définit la date de début prévue à la date actuelle
                self.temps_estime_prevu = self.temps_estime # On définit le temps estimé prévu au temps estimé
                self.temps_restant_prevu = self.temps_estime #...

        super().save(*args, **kwargs) # On sauvegarde la tâche avec les modifications apportées


class Event(models.Model):
    """
    Modèle pour les événements
    """
    title = models.CharField(max_length=200) # Titre de l'événement
    start_date = models.DateTimeField() # Date de début de l'événement
    end_date = models.DateTimeField() # Date de fin de l'événement
    project = models.ForeignKey(Project, on_delete=models.CASCADE) # Projet lié à l'événement
    task = models.ForeignKey(Task, on_delete=models.CASCADE) # Tâche liée à l'événement
    user = models.ForeignKey(User, on_delete=models.CASCADE) # Utilisateur lié à l'événement
    comments = models.TextField(blank=True) # Commentaires liés à l'événement
