from django.urls import path
from .views import ProjectListView, ProjectCreateView, calendar, TaskListView, add_task_comment, TaskDetailView, \
    SignUpView, all_notifications, project_detail, TaskCreateView, TaskUpdateView, profile, event_api

urlpatterns = [

    # Task URLs
    path('tasks/', TaskListView.as_view(), name='task_list'),  # lister toutes les tâches
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),  # detailler une tâche
    path('tasks/create/<int:project_id>/', TaskCreateView.as_view(), name='task_create'),  # créer une tâche
    path('tasks/<int:pk>/add-comment/', add_task_comment, name='task_add_comment'),
    # ajouter un commentaire à une tâche
    path('tasks/by-status/', TaskListView.as_view(), name='task_list_by_status'),  # lister toutes les tâches par status
    path('tasks/by-priority/', TaskListView.as_view(), name='task_list_by_priority'),
    # lister toutes les tâches par priorité
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),  # mettre à jour une tâche

    # Project URLs
    path('', ProjectListView.as_view(), name='project_list_by_start_date'),  # lister tous les projets par date de début
    path('create/', ProjectCreateView.as_view(), name='project_create'),  # créer un projet
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
]
