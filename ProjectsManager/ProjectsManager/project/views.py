from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Project, Task, Event
from .forms import ProjectForm, TaskForm

class HomePageView(TemplateView):
    template_name = 'home.html'


class ProjectListView(ListView):
    model = Project
    template_name = 'project/project_list.html'
    ordering = ['-start_date']

    def get_queryset(self):
        return Project.objects.all()
        # return Project.objects.filter(assigned_to=self.request.user)


class ProjectCreateView(CreateView):
    model = Project
    template_name = 'project/project_create.html'
    fields = ['name', 'description', 'assigned_to', 'start_date', 'end_date']
    success_url = reverse_lazy('project_list_by_start_date')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.pk})


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'project/task_create.html'
    success_url = reverse_lazy('project_list')

    #def get_initial(self):
    #    project = get_object_or_404(Project, pk=self.kwargs['project_id'])
    #    return {'project': project}

    def form_valid(self, form):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        form.instance.created_by = self.request.user
        #form.instance.project_id = get_object_or_404(Project, pk=self.kwargs['project_id'])
        form.instance.project = project
        print(form.instance.project) # <Project: Project 1>
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = ProjectForm()
        return context


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


def calendar_view(request):
    # Récupérer toutes les tâches et tous les projets
    tasks = Task.objects.all()
    projects = Project.objects.all()

    # Liste des événements à afficher sur le calendrier
    events = []

    # Parcourir toutes les tâches pour créer des événements correspondants
    for task in tasks:
        events.append({
            'title': task.name,
            'start': task.start_date.isoformat(),
            'end': task.end_date.isoformat(),
            'type': 'task'
        })

    # Parcourir tous les projets pour créer des événements correspondants
    for project in projects:
        events.append({
            'title': project.name,
            'start': project.start_date.isoformat(),
            'end': project.end_date.isoformat(),
            'type': 'project'
        })

    # Tri des événements par date de début
    events = sorted(events, key=lambda e: e['start'])

    # Ajout d'une couleur pour chaque type d'événement
    colors = {'project': '#007bff', 'task': '#28a745'}
    for event in events:
        event['color'] = colors.get(event['type'])

    # Rendu du template
    context = {'events': events}
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


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


@login_required
def all_notifications(request):
    return render(request, 'all_notifications.html')


def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    tasks = Task.objects.filter(project=project)
    context = {
        'project': project,
        'tasks': tasks,
    }
    return render(request, 'project/project_detail.html', context)


def calendar_view(request):
    events = Event.objects.all()
    event_list = []
    for event in events:
        event_list.append({
            'title': event.title,
            'start': event.start_date,
            'end': event.end_date,
        })
    return render(request, 'project/calendar.html', {'events': event_list})

def get_calendar_events():
    projects = Project.objects.all()
    tasks = Task.objects.all()
    rows = []
    for project in projects:
        row = []
        row.append('<td class="project">' + project.name + '</td>')
        row.append('<td class="project-start">' + str(project.start_date) + '</td>')
        row.append('<td class="project-end">' + str(project.end_date) + '</td>')
        row.append('<td class="project-type">Projet</td>')
        rows.append('<tr>' + ''.join(row) + '</tr>')

    for task in tasks:
        row = []
        row.append('<td class="task">' + task.name + '</td>')
        row.append('<td class="task-start">' + str(task.start_date) + '</td>')
        row.append('<td class="task-end">' + str(task.end_date) + '</td>')
        row.append('<td class="task-type">Tâche</td>')
        rows.append('<tr>' + ''.join(row) + '</tr>')

    return '\n'.join(rows)


def event_api(request):

    event_list = get_calendar_events()
    context = {'event_list': event_list}
    return render(request, 'project/calendar.html', context)