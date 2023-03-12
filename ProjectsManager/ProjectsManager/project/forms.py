from django import forms
from django.contrib.auth.models import User
from django.forms.widgets import SelectDateWidget, DateInput
from .models import Project, Task
from datetime import datetime


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
    class Meta:
        model = Task
        exclude = ['project', 'temps_estime', 'temps_passe', 'temps_restant', 'date_modification', 'date_fin_reelle',
                   'temps_reel', 'temps_restant_reel', 'temps_estime_reel', 'temps_passe_reel', 'avancement_reel',
                   'date_debut_reelle', 'temps_estime_prevu',
                   'temps_restant_prevu', 'temps_passe_prevu']
        fields = ['name', 'description', 'assigned_to', 'start_date', 'end_date', 'priority', 'status', 'comments',
                  'user', 'type', 'avancement', 'date_debut_prevue', 'date_fin_prevue']

    def __init__(self, *args, **kwargs):
        project_id = kwargs.pop('project_id', None)
        super().__init__(*args, **kwargs)
        self.fields['date_debut_prevue'].widget = SelectDateWidget()
        self.fields['date_debut_prevue'].initial = datetime.now()
        self.fields['date_fin_prevue'].widget = SelectDateWidget()
        self.fields['date_fin_prevue'].initial = datetime.now()
