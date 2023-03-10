from django.urls import path
from .views import (
    ProjectListView, ProjectCreateView, ProjectUpdateView, project_detail, ProjectDeleteView,
    calendar,
    TaskListView, add_task_comment, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    SignUpView,
    MessageCreateView,
    MessageDetailView,
    profile,
    event_api,
    all_notifications,
)

urlpatterns = [

    # Task URLs
    path('tasks/', TaskListView.as_view(), name='task_list'),  # lister toutes les tâches
    path('tasks/<int:project_id>/<int:task_id>/', TaskDetailView.as_view(), name='task_detail'),
    # detailler une tâche
    path('tasks/create/<int:project_id>/', TaskCreateView.as_view(), name='task_create'),  # créer une tâche
    path('tasks/<int:pk>/add-comment/', add_task_comment, name='task_add_comment'),
    # ajouter un commentaire à une tâche
    path('tasks/by-status/', TaskListView.as_view(), name='task_list_by_status'),  # lister toutes les tâches par status
    path('tasks/by-priority/', TaskListView.as_view(), name='task_list_by_priority'),
    # lister toutes les tâches par priorité
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),  # mettre à jour une tâche
    # supprimer une tâche
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),  # supprimer une tâche

    # Project URLs
    path('', ProjectListView.as_view(), name='project_list_by_start_date'),  # lister tous les projets par date de début
    path('<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update'),  # mettre à jour un projet
    path('create/', ProjectCreateView.as_view(), name='project_create'),  # créer un projet
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),  # supprimer un projet
    path('project_detail/<int:pk>/', project_detail, name='project_detail'),  # détaller un projet
    path('projects/', ProjectListView.as_view(), name='project_list'),  # lister tous les projets
    path('projects/by-start-date/', ProjectListView.as_view(), name='project_list_by_start_date'),
    # lister tous les projets par date de début

    # Calendar URLs
    # path('calendar/', calendar_view, name='project_calendar'),
    path('calendar/', calendar, name='calendar'),  # afficher le calendrier
    path('event_api', event_api, name='event_api'),  # API pour le calendrier
    # autres URLs
    path('signup/', SignUpView.as_view(), name='signup'),  # s'inscrire
    path('notifications/', all_notifications, name='all_notifications'),  # afficher toutes les notifications
    path('profile/', profile, name='profile'),  # afficher le profil de l'utilisateur

    # Message URLs
    path('messages/create/<int:project_id>/', MessageCreateView.as_view(), name='message_create'),

]
