from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import SelectDateWidget, DateInput
from .models import Project, Task
from datetime import datetime, timezone


class ProjectForm(forms.ModelForm):
    """
    Formulaire de création et de modification de projet
    """
    start_date = forms.DateField(widget=SelectDateWidget(
        attrs={'class': 'custom-select'}))  # widget=SelectDateWidget permet de créer un selecteur de date
    end_date = forms.DateField(widget=SelectDateWidget(
        attrs={'class': 'custom-select'}))  # widget=SelectDateWidget permet de créer un selecteur de date
    assigned_to = forms.ModelMultipleChoiceField(  # permet de créer un selecteur multiple
        queryset=User.objects.all(),  # queryset=User.objects.all() permet de récupérer tous les utilisateurs
        widget=forms.SelectMultiple(attrs={'class': 'custom-select'}),
        # widget=forms.SelectMultiple permet de créer un selecteur multiple
        required=False  # required=False permet de rendre le champ facultatif
    )

    class Meta:
        """
        Classe Meta qui permet de définir les paramètres du formulaire (model, champs, widgets)
        """
        model = Project  # Le model sur lequel on va travailler
        fields = ['name', 'description', 'assigned_to', 'start_date',
                  'end_date']  # Les champs du model sur lesquels on va travailler


class ProjectSearchForm(forms.Form):
    """
    Formulaire de recherche de projet
    """
    q = forms.CharField(label='Rechercher un projet',
                        # label='Rechercher un projet' permet de définir le label du champ
                        max_length=100,  # max_length=100 permet de définir la longueur maximale du champ
                        widget=forms.TextInput(attrs={'class': 'form-control mr-sm-2',
                                                      # widget=forms.TextInput permet de créer un champ de texte
                                                      'type': 'search',
                                                      # 'type': 'search' permet de définir le type du champ
                                                      'placeholder': 'Rechercher un projet',
                                                      # 'placeholder': 'Rechercher un projet' permet de définir le placeholder du champ
                                                      })
                        )


class TaskForm(forms.ModelForm):
    PRIORITY_CHOICES = [(1, 'Faible'), (2, 'Moyenne'), (3, 'Haute'), (4, 'Urgente'),
                        (5, 'Critique')]  # Définition des choix pour les champs de type ChoiceField
    STATUS_CHOICES = [(1, 'A faire'), (2, 'En cours'),
                      (3, 'Terminée')]  # Définition des choix pour les champs de type ChoiceField

    name = forms.CharField(max_length=255,
                           label='Nom de la tâche')  # label='Nom de la tâche' permet de définir le label du champ
    description = forms.CharField(widget=forms.Textarea,
                                  label='Description')  # widget=forms.Textarea permet de créer un champ de texte multiligne
    assigned_to = forms.ModelChoiceField(queryset=User.objects.all(),
                                         label='Assignée à')  # queryset=User.objects.all() permet de récupérer tous les utilisateurs
    start_date = forms.DateField(widget=forms.DateField(widget=forms.SelectDateWidget(),
                                                        label='Date de début'))  # widget=forms.SelectDateWidget() permet de créer un selecteur de date
    end_date = forms.DateField(widget=forms.DateField(widget=forms.SelectDateWidget(),
                                                      label='Date de fin'))  # widget=forms.SelectDateWidget() permet de créer un selecteur de date
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES,
                                 label='Priorité')  # label='Priorité' permet de définir le label du champ
    status = forms.ChoiceField(choices=STATUS_CHOICES,
                               label='Statut')  # label='Statut' permet de définir le label du champ
    comments = forms.CharField(widget=forms.Textarea, required=False,
                               label='Commentaires')  # required=False permet de rendre le champ facultatif

    class Meta:
        model = Task
        exclude = ['project', 'temps_estime', 'temps_passe', 'temps_restant', 'date_modification', 'date_fin_reelle',
                   'temps_reel', 'temps_restant_reel', 'temps_estime_reel', 'temps_passe_reel', 'avancement_reel',
                   'date_debut_reelle', 'temps_estime_prevu']  # exclude permet d'exclure des champs du formulaire
        fields = ['name', 'description', 'assigned_to', 'start_date', 'end_date', 'priority', 'status', 'comments',
                  'user', 'type', 'avancement', 'date_debut_prevue', 'date_fin_prevue', 'temps_estime',
                  'temps_passe_prevu',
                  'temps_restant_prevu']  # fields permet de définir les champs du formulaire

    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id', None)  # On récupère l'id du projet
        super().__init__(*args, **kwargs)  # On appelle le constructeur de la classe parente
        self.fields['date_debut_prevue'].widget = SelectDateWidget()  # On définit le widget du champ date_debut_prevue
        self.fields['date_debut_prevue'].initial = datetime.now()  # On initialise la date de début à la date du jour
        self.fields['date_fin_prevue'].widget = SelectDateWidget()  # On définit le widget du champ date_fin_prevue
        self.fields['date_fin_prevue'].initial = datetime.now()  # On initialise la date de fin à la date du jour

    def label_from_instance(self, obj):
        """
        Permet de définir le label des champs de type ModelChoiceField
        :param obj:
        :return:
        """
        return f"{obj.first_name} {obj.last_name}"  # On retourne le nom et le prénom de l'utilisateur
