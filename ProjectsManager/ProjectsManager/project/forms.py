from django import forms
from django.forms.widgets import SelectDateWidget
from .models import Project, Task


class ProjectForm(forms.ModelForm):
    start_date = forms.DateField(widget=SelectDateWidget)
    end_date = forms.DateField(widget=SelectDateWidget)

    class Meta:
        model = Project
        fields = ['name', 'description', 'assigned_to', 'start_date', 'end_date']


class TaskForm(forms.ModelForm):
    start_date = forms.DateField(widget=SelectDateWidget)
    end_date = forms.DateField(widget=SelectDateWidget)

    class Meta:
        model = Task
        fields = ['name', 'description', 'assigned_to', 'start_date', 'end_date', 'priority', 'status']
