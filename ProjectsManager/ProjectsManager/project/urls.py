from django.urls import path
from .views import ProjectListView, ProjectCreateView, calendar_view, TaskListView, add_task_comment, TaskDetailView, calendar

urlpatterns = [
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/add-comment/', add_task_comment, name='task_add_comment'),
    path('tasks/by-status/', TaskListView.as_view(), name='task_list_by_status'),
    path('tasks/by-priority/', TaskListView.as_view(), name='task_list_by_priority'),
    path('projects/by-start-date/', ProjectListView.as_view(), name='project_list_by_start_date'),
    path('projects/create/', ProjectCreateView.as_view(), name='project_create'),
    # path('calendar/', calendar_view, name='project_calendar'),
    path('calendar/', calendar, name="calendar"),
]
