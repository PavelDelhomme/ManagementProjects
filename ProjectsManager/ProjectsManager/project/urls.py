from django.urls import path
from .views import (
    ProjectListView, ProjectCreateView, ProjectUpdateView, ProjectDetailView, ProjectDeleteView,
    calendar,
    TaskListView, add_task_comment, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    SignUpView,
    profile,
    event_api,
    MarkTaskAsCompletedView, MarkTaskAsIncompleteView,
    ProjectSearchView,
    page_not_found
)

urlpatterns = [

    # Task URLs
    path('tasks/', TaskListView.as_view(), name='task_list'), # liste des tâches
    path('tasks/<int:project_id>/<int:task_id>/', TaskDetailView.as_view(), name='task_detail'), # détail d'une tâche
    path('tasks/create/<int:project_id>/', TaskCreateView.as_view(), name='task_create'), # création d'une tâche
    path('tasks/<int:pk>/add-comment/', add_task_comment, name='task_add_comment'), # ajout d'un commentaire à une tâche
    path('tasks/<int:project_id>/completed/<int:task_id>/', MarkTaskAsCompletedView.as_view(),
         name='mark_task_as_completed'), # marquer une tâche comme terminée
    path('tasks/<int:project_id>/incompleted/mark_task_as_incompleted/<int:task_id>/',
         MarkTaskAsIncompleteView.as_view(), name='mark_task_as_incompleted'), # marquer une tâche comme non terminée
    # path('tasks/<int:pk>/uncomplete/', uncomplete_task, name='task_uncomplete'),
    path('tasks/by-status/', TaskListView.as_view(), name='task_list_by_status'), # liste des tâches par statut
    path('tasks/by-priority/', TaskListView.as_view(), name='task_list_by_priority'), # liste des tâches par priorité
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'), # mise à jour d'une tâche
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'), # suppression d'une tâche

    # Project URLs
    path('', ProjectListView.as_view(), name='project_list_by_start_date'), # liste des projets par date de début
    path('<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update'), # mise à jour d'un projet
    path('create/', ProjectCreateView.as_view(), name='project_create'), # création d'un projet
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'), # suppression d'un projet
    path('project_detail/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'), # détail d'un projet
    path('projects/', ProjectListView.as_view(), name='project_list'), # liste des projets
    path('projects/by-start-date/', ProjectListView.as_view(), name='project_list_by_start_date'), # liste des projets par date de début

    # Project Search URLs
    path('search/', ProjectSearchView.as_view(), name='project_search'), # recherche de projets

    # Calendar URLs
    path('calendar/', calendar, name='calendar'), # calendrier
    path('tasklistapi/', event_api, name='event_api'), # API pour le calendrier
    # autres URLs
    path('signup/', SignUpView.as_view(), name='signup'), # inscription
    path('profile/', profile, name='profile'), # profil

]

handler404 = 'project.views.page_not_found' # page 404 personnalisée
