from django import forms
from django.forms.widgets import SelectDateWidget
from .models import Project, Task, Message


class ProjectForm(forms.ModelForm):
    """
    Form for creating a new project
    """
    start_date = forms.DateField(
        widget=SelectDateWidget)  # SelectDateWidget est un widget qui permet de selectionner une date depuis le menu dopdown
    end_date = forms.DateField(
        widget=SelectDateWidget)  # SelectDateWidget est un widget qui permet de selectionner une date depuis le menu dopdown

    class Meta:
        model = Project  # Le model sur lequel on va travailler
        fields = ['name', 'description', 'assigned_to', 'start_date',
                  'end_date']  # Les champs du model sur lesquels on va travailler


class TaskForm(forms.ModelForm):
    """
    Form for creating a new task
    """
    start_date = forms.DateField(widget=SelectDateWidget)
    end_date = forms.DateField(widget=SelectDateWidget)

    class Meta:
        model = Task
        fields = ['name', 'description', 'assigned_to', 'start_date', 'end_date', 'priority', 'status']


class MessageForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=True)
    recipient_id = forms.IntegerField(widget=forms.HiddenInput())  # nouveau champ caché pour stocker l'identifiant du destinataire

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    class Meta:
        model = Message
        fields = ['content', 'recipient_id']
