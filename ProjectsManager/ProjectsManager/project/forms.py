from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import SelectDateWidget, DateInput
from .models import Project, Task
from datetime import datetime, timezone


class ProjectForm(forms.ModelForm):
    """
    Form for creating a new project
    """
    start_date = forms.DateField(widget=SelectDateWidget(attrs={'class': 'custom-select'}))
    end_date = forms.DateField(widget=SelectDateWidget(attrs={'class': 'custom-select'}))
    assigned_to = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'custom-select'}),
        required=False
    )

    class Meta:
        model = Project  # Le model sur lequel on va travailler
        fields = ['name', 'description', 'assigned_to', 'start_date',
                  'end_date']  # Les champs du model sur lesquels on va travailler


class ProjectSearchForm(forms.Form):
    q = forms.CharField(label='Rechercher un projet',
                        max_length=100,
                        widget=forms.TextInput(attrs={'class': 'form-control mr-sm-2',
                                                      'type': 'search',
                                                      'placeholder': 'Rechercher un projet',
                                                      })
                        )


# class TaskForm(forms.ModelForm):
#    """
#    Form for creating a new task
#    """
#    start_date = forms.DateField(widget=SelectDateWidget)
#    end_date = forms.DateField(widget=SelectDateWidget)
#    assigned_to = forms.ModelMultipleChoiceField(
#        queryset=User.objects.all(),
#        widget=forms.CheckboxSelectMultiple,
#        required=False
#    )
#    created_at = forms.DateField(widget=SelectDateWidget)
#    project = forms.IntegerField(widget=forms.HiddenInput())

# Ajout de la zone de texte cachée pour l'ID de projet
#   project_id = forms.IntegerField(widget=forms.HiddenInput())

#   class Meta:
#        model = Task
#        fields = ['name', 'description', 'assigned_to', 'start_date', 'end_date', 'priority', 'status', 'comments',
#                  'user', 'type', 'avancement', 'temps_restant', 'date_fin_reelle', 'temps_reel', 'temps_restant_reel',
#                  'temps_estime_reel', 'temps_passe_reel', 'avancement_reel', 'date_debut_reelle',
#                  'date_fin_prevue', 'temps_estime_prevu', 'temps_restant_prevu', 'temps_passe_prevu',
#                  'date_debut_prevue', 'project']
#        widgets = {
#            "start_date": DateInput(),
#            "end_date": DateInput(),
#        }

"""
class TaskForm(forms.ModelForm):
    """
# Form for creating a new task
"""
assigned_to = forms.ModelMultipleChoiceField(
    queryset=None,
    widget=forms.CheckboxSelectMultiple,
    required=False
)

start_date = forms.DateField(widget=SelectDateWidget())
end_date = forms.DateField(widget=SelectDateWidget())

class Meta:
    model = Task
    fields = ['name', 'description', 'assigned_to', 'start_date', 'end_date', 'priority', 'status', 'comments']

def __init__(self, *args, **kwargs):
    self.project = kwargs.pop('project', None)
    super().__init__(*args, **kwargs)
    if self.project:
        self.fields['assigned_to'].queryset = self.project.members.all()
"""


class TaskForm(forms.ModelForm):
    PRIORITY_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    STATUS_CHOICES = [(1, 'A faire'), (2, 'En cours'), (3, 'Terminée')]

    name = forms.CharField(max_length=255, label='Nom de la tâche')
    description = forms.CharField(widget=forms.Textarea, label='Description')
    assigned_to = forms.ModelChoiceField(queryset=User.objects.all(), label='Assignée à')
    start_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), label='Date de début')
    end_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), label='Date de fin')
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, label='Priorité')
    status = forms.ChoiceField(choices=STATUS_CHOICES, label='Statut')
    comments = forms.CharField(widget=forms.Textarea, required=False, label='Commentaires')

    class Meta:
        model = Task
        exclude = ['project', 'temps_estime', 'temps_passe', 'temps_restant', 'date_modification', 'date_fin_reelle',
                   'temps_reel', 'temps_restant_reel', 'temps_estime_reel', 'temps_passe_reel', 'avancement_reel',
                   'date_debut_reelle', 'temps_estime_prevu']
        fields = ['name', 'description', 'assigned_to', 'start_date', 'end_date', 'priority', 'status', 'comments',
                  'user', 'type', 'avancement', 'date_debut_prevue', 'date_fin_prevue', 'temps_estime',
                  'temps_passe_prevu',
                  'temps_restant_prevu']

    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id', None)
        super().__init__(*args, **kwargs)
        self.fields['date_debut_prevue'].widget = SelectDateWidget()
        self.fields['date_debut_prevue'].initial = datetime.now()
        self.fields['date_fin_prevue'].widget = SelectDateWidget()
        self.fields['date_fin_prevue'].initial = datetime.now()

# Class TaskForm

# name = forms.CharField(label='Nom', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
# description = forms.CharField(label='Description', max_length=1000,
#                                widget=forms.Textarea(attrs={'class': 'form-control'}))
# assigned_to = forms.ModelMultipleChoiceField(
#    queryset=User.objects.all(),
#    widget=forms.SelectMultiple(attrs={'class': 'custom-select'}),
#    required=False
# )
# start_date = forms.DateField(label='Date de début', widget=SelectDateWidget(attrs={'class': 'custom-select'}))
# end_date = forms.DateField(label='Date de fin', widget=SelectDateWidget(attrs={'class': 'custom-select'}))
# priority = forms.ChoiceField(label='Priorité', choices=PRIORITY_CHOICES, widget=forms.Select(attrs={'class': 'custom-select'}))
# status = forms.ChoiceField(label='Statut', choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'custom-select'}))
# comments = forms.CharField(label='Commentaires', max_length=1000,
#                             widget=forms.Textarea(attrs={'class': 'form-control'}))
# user = forms.ModelChoiceField(label='Utilisateur', queryset=User.objects.all(),
#                                widget=forms.Select(attrs={'class': 'custom-select'}))
# type = forms.ChoiceField(label='Type', choices=TYPE_CHOICES, widget=forms.Select(attrs={'class': 'custom-select'}))
# avancement = forms.ChoiceField(label='Avancement', choices=AVANCEMENT_CHOICES,
#                                widget=forms.Select(attrs={'class': 'custom-select'}))
# date_debut_prevue = forms.DateField(label='Date de début prévue', widget=SelectDateWidget(attrs={'class': 'custom-select'}))
# date_fin_prevue = forms.DateField(label='Date de fin prévue', widget=SelectDateWidget(attrs={'class': 'custom-select'}))
# temps_estime = forms.CharField(label='Temps estimé', max_length=100,
#                                widget=forms.TextInput(attrs={'class': 'form-control'}))
# temps_passe = forms.CharField(label='Temps passé', max_length=100,
#                                widget=forms.TextInput(attrs={'class': 'form-control'}))
# temps_restant = forms.CharField(label='Temps restant', max_length=100,
#                                widget=forms.TextInput(attrs={'class': 'form-control'}))
# date_modification = forms.DateField(label='Date de modification', widget=SelectDateWidget(attrs={'class': 'custom-select'}))
# date_fin_reelle = forms.DateField(label='Date de fin réelle', widget=SelectDateWidget(attrs={'class': 'custom-select'}))
# temps_reel = forms.CharField(label='Temps réel', max_length=100,
#                                widget=forms.TextInput(attrs={'class': 'form-control'}))
# temps_restant_reel = forms.CharField(label='Temps restant réel', max_length=100,
#                                widget=forms.TextInput(attrs={'class': 'form-control'}))
# temps_estime_reel = forms.CharField(label='Temps estimé réel', max_length=100,
#                                widget=forms.TextInput(attrs={'class': 'form-control'}))
# temps_passe_reel = forms.CharField(label='Temps passé réel', max_length=100,
#                                widget=forms.TextInput(attrs={'class': 'form-control'}))
# avancement_reel = forms.ChoiceField(label='Avancement réel', choices=AVANCEMENT_CHOICES,
#                                widget=forms.Select(attrs={'class': 'custom-select'}))
# date_debut_reelle = forms.DateField(label='Date de début réelle', widget=SelectDateWidget(attrs={'class': 'custom-select'}))
# temps_estime_prevu = forms.CharField(label='Temps estimé prévu', max_length=100,
#                                widget=forms.TextInput(attrs={'class': 'form-control'}))
# temps_passe_prevu = forms.CharField(label='Temps passé prévu', max_length=100,
#                                widget=forms.TextInput(attrs={'class': 'form-control'}))
# temps_restant_prevu = forms.CharField(label='Temps restant prévu', max_length=100,
#                                widget=forms.TextInput(attrs={'class': 'form-control'}))
