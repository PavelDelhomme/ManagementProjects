from django.contrib import admin
from .models import *

from ProjectsManager.core.projects.models import *
from ProjectsManager.core.manager.models import *
from ProjectsManager.core.register.models import *
from ProjectsManager.core.tasks.models import *
from ProjectsManager.core.users.models import *

admin.site.register(Project)
admin.site.register()
admin.site.register(Profile)
admin.site.register(Task)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')

admin.site.register(CustomUser, CustomUserAdmin)

class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

admin.site.register(CustomGroup, CustomGroupAdmin)

class CustomPermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type', 'codename')
    search_fields = ('name', 'content_type__model', 'codename')

admin.site.register(CustomPermission, CustomPermissionAdmin)

