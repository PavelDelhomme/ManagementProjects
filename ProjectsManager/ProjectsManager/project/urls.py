from django.urls import path
from .views import (
    ProjectListView, ProjectCreateView, ProjectUpdateView, project_detail, ProjectDeleteView,
    calendar,
    TaskListView, add_task_comment, TaskDetailView, TaskCreateView, TaskUpdateView, TaskDeleteView,
    SignUpView,
    profile,
    event_api,
    all_notifications,
    complete_task,
)

urlpatterns = [

    # Task URLs
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/<int:project_id>/<int:task_id>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/create/<int:project_id>/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/add-comment/', add_task_comment, name='task_add_comment'),
    path('tasks/<int:pk>/complete/', complete_task, name='task_complete'),
    # path('tasks/<int:pk>/uncomplete/', uncomplete_task, name='task_uncomplete'),
    path('tasks/by-status/', TaskListView.as_view(), name='task_list_by_status'),
    path('tasks/by-priority/', TaskListView.as_view(), name='task_list_by_priority'),
    path('tasks/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),

    # Project URLs
    path('', ProjectListView.as_view(), name='project_list_by_start_date'),
    path('<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
    path('project_detail/<int:pk>/', project_detail, name='project_detail'),
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/by-start-date/', ProjectListView.as_view(), name='project_list_by_start_date'),

    # Calendar URLs
    path('calendar/', calendar, name='calendar'),
    path('event_api', event_api, name='event_api'),
    # autres URLs
    path('signup/', SignUpView.as_view(), name='signup'),
    path('notifications/', all_notifications, name='all_notifications'),
    path('profile/', profile, name='profile'),
]
