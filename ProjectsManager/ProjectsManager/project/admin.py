from django.contrib import admin
from .models import Project, Task, Event

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'start_date', 'end_date')
    search_fields = ('name', 'description', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'project', 'status')
    search_fields = ('name', 'project__name')
    list_filter = ('status',)
