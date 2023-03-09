from django.urls import path
from .views import ProjectListView, ProjectCreateView, calendar_view, TaskListView, add_task_comment, TaskDetailView, \
    calendar, SignUpView, all_notifications, project_detail, event_api, TaskCreateView

urlpatterns = [
    # Task URLs
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/create/<int:project_id>/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/add-comment/', add_task_comment, name='task_add_comment'),
    path('tasks/by-status/', TaskListView.as_view(), name='task_list_by_status'),
    path('tasks/by-priority/', TaskListView.as_view(), name='task_list_by_priority'),
    # Project URLs
    path('', ProjectListView.as_view(), name='project_list_by_start_date'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('project_detail/<int:pk>/', project_detail, name='project_detail'),
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/by-start-date/', ProjectListView.as_view(), name='project_list_by_start_date'),
    # path('projects/create/', ProjectCreateView.as_view(), name='project_create'),
    # Calendar URLs
    # path('calendar/', calendar_view, name='project_calendar'),
    path('calendar/', calendar_view, name="calendar"),
    path('event_api/', event_api, name="event_api"),
    # autres URLs
    path('signup/', SignUpView.as_view(), name='signup'),
    path('notifications/', all_notifications, name='all_notifications'),
]
