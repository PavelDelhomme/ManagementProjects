from django import forms
from .models import Project, Task, ProjectFile, TaskFile


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'assigned_users', 'assigned_groups']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'due_date', 'assigned_users', 'project']


class ProjectFileForm(forms.ModelForm):
    class Meta:
        model = ProjectFile
        fields = ['name', 'description', 'file']


class TaskFileForm(forms.ModelForm):
    class Meta:
        model = TaskFile
        fields = ['name', 'description', 'file']
