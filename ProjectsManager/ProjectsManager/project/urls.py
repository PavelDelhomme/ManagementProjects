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
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('tasks/<int:project_id>/<int:task_id>/', TaskDetailView.as_view(), name='task_detail'),
    path('tasks/create/<int:project_id>/', TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/add-comment/', add_task_comment, name='task_add_comment'),
    path('tasks/<int:project_id>/completed/<int:task_id>/', MarkTaskAsCompletedView.as_view(),
         name='mark_task_as_completed'),
    path('tasks/<int:project_id>/incompleted/mark_task_as_incompleted/<int:task_id>/',
         MarkTaskAsIncompleteView.as_view(), name='mark_task_as_incompleted'),
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
    path('project_detail/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
    path('projects/', ProjectListView.as_view(), name='project_list'),
    path('projects/by-start-date/', ProjectListView.as_view(), name='project_list_by_start_date'),

    # Project Search URLs
    path('search/', ProjectSearchView.as_view(), name='project_search'),

    # Calendar URLs
    path('calendar/', calendar, name='calendar'),
    path('event_api', event_api, name='event_api'),
    # autres URLs
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', profile, name='profile'),

]

handler404 = 'project.views.page_not_found'
