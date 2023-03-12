from django.contrib import admin
from .models import Project, Task, Event
from django_admin_listfilter_dropdown.filters import DropdownFilter


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin View for Project
    """
    list_display = ('id', 'name', 'description', 'start_date', 'end_date')
    search_fields = ('name', 'description', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin View for Task
    """
    list_display = ('id', 'name', 'description', 'project', 'status')
    search_fields = ('name', 'project__name')
    list_filter = ('status',)
