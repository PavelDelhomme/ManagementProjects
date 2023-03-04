from django.urls import path
from . import views

# app_name = 'projects'

urlpatterns = [
    path('projects_list', views.ProjectListView.as_view(), name='projects_list'),
    path('create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
    path('<int:pk>/task/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('<int:project_pk>/task/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('<int:project_pk>/task/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('<int:project_pk>/task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
]
