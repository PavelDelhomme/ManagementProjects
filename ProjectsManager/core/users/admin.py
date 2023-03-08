from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import CustomPermission, CustomUser, CustomGroup, UserProfile



class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'bio')
    search_fields = ('email', 'first_name', 'last_name', 'bio')
    form = UserChangeForm
    add_form = UserCreationForm

class CustomGroupUserInline(admin.TabularInline):
    model = CustomGroup.user_set.through

class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    inlines = [
        CustomGroupUserInline,
    ]


class CustomPermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type', 'codename', 'description')
    search_fields = ('name', 'content_type__model', 'codename', 'description')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_pic')


admin.site.unregister(Group)


admin.site.register(CustomGroup, CustomGroupAdmin)
admin.site.register(CustomPermission, CustomPermissionAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
