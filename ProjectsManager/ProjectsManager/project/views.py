from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.views.generic import ListView
from django.urls import reverse_lazy
from .models import Project, Task


@login_required
def calendar_view(request):
    projects = Project.objects.all()
    tasks = Task.objects.all()
    context = {
        'projects': projects,
        'tasks': tasks,
    }
    return render(request, 'project/calendar.html', context)


@login_required
def add_task_comment(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.comments = request.POST['comments']
        task.save()
    context = {
        'task': task,
    }
    return render(request, 'project/task_detail.html', context)


class ProjectListView(ListView):
    model = Project
    template_name = 'project/project_list.html'
    ordering = ['-start_date']


class ProjectCreateView(CreateView):
    model = Project
    template_name = 'project/project_create.html'
    fields = ['name', 'description', 'assigned_to', 'start_date', 'end_date']
    success_url = reverse_lazy('project_list_by_start_date')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TaskCreateView(CreateView):
    modeal = Task
    template_name = 'project/task_create.html'
    fields = ['name', 'description', 'assigned_to', 'project', 'start_date', 'end_date']
    success_url = reverse_lazy('project_list_by_start_date')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TaskListView(ListView):
    model = Task
    template_name = 'project/task_list.html'
    # ordering = ['-start_date']
    ordering = ['-status', '-priority', '-start_date']


class TaskDetailView(ListView):
    model = Task
    template_name = 'project/task_detail.html'

def calendar(request):
    projects = Project.objects.all()
    tasks = Task.objects.all()
    context = {
        'projects': projects,
        'tasks': tasks,
    }
    return render(request, 'project/calendar.html', context)