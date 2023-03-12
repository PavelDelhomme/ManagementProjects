from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView
from django.views.generic import CreateView, UpdateView, DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, Http404
from .models import Project, Task, Event
from .forms import ProjectForm, TaskForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from django.contrib.auth import get_user_model

User = get_user_model()


class HomePageView(TemplateView):
    template_name = 'home.html'  # Le template qui va etre affiche dans la page home

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        context['tasks'] = Task.objects.all()
        context['task_due_today'] = Task.objects.filter(end_date=timezone.now().date())
        context['task_overdue'] = Task.objects.filter(end_date__lt=timezone.now().date())
        context['completed_tasks'] = Task.objects.filter(status='complete')
        return context


class ProjectListView(ListView):
    model = Project
    template_name = 'project/project_list.html'
    ordering = ['-start_date']

    def get_queryset(self):
        return Project.objects.filter(
            assigned_to=self.request.user)


class ProjectCreateView(CreateView):
    model = Project
    template_name = 'project/project_create.html'
    fields = ['name', 'description', 'assigned_to', 'start_date',
              'end_date']
    success_url = reverse_lazy(
        'project_list_by_start_date')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.pk})


class ProjectUpdateView(UpdateView):
    model = Project
    fields = ['name', 'description', 'assigned_to', 'start_date', 'end_date', 'comments']
    template_name = 'project/project_update.html'
    success_url = reverse_lazy('project_list_by_start_date')

    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'project/project_delete.html'
    success_url = reverse_lazy('project_list_by_start_date')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Le projet a été supprimé avec succès.')
        return super().delete(request, *args, **kwargs)

    def get_context_object_name(self, queryset=None):
        obj = super().get_oject(queryset=queryset)
        if not obj.can_be_deleted_by(self.request.user):
            raise Http404
        return obj


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project/project_detail.html'
    context_object_name = 'project'

    def get(self, request, *args, **kwargs):
        project = self.get_object()
        # self.request.session['project_id'] = project.id
        self.request.session['project_id'] = self.kwargs['pk']
        if not project.can_be_viewed_by(request.user):
            raise Http404
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs['pk']
        context['project'] = Project.objects.get(id=project_id)
        context['tasks'] = Task.objects.filter(project=project_id)
        # project = self.get_object()
        # context['tasks'] = project.tasks()
        # context['form'] = TaskForm(initial={'project': project})
        return context


class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'project/task_create.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return context

    def form_valid(self, form):
        form.instance.project_id = self.kwargs['project_id']
        return super().form_valid(form)

    # model = Task
    # form_class = TaskForm
    # template_name = 'project/task_create.html'
    # success_url = reverse_lazy('project_list')

    # Mettre à jour la méthode form_valid() pour inclure l'ID du projet
    # def get(self, request, project_id):
    #    project = get_object_or_404(Project, pk=project_id)
    #    form = TaskForm()
    #    print(project_id)
    #    return render(request, self.template_name, {'form': form, 'project': project})

    # def form_valid(self, form):
    #    project_id = self.request.session.get('project_id') or self.kwargs['project_id']
    #    form.instance.project = Project.objects.get(pk=project_id)

    # project = get_object_or_404(Project, id=self.kwargs['project_id'])
    # form.instance.created_by = self.request.user
    # form.instance.project = project
    # messages.success(self.request, 'La tâche a été créée avec succès.')
    #    return super().form_valid(form)

    # def get_success_url(self):
    #    project_id = self.request.session.get('project_id') or self.kwargs['project_id']
    #    return reverse('project_detail', kwargs={'pk': project_id})
    # return reverse('project_detail', kwargs={'project_id': self.kwargs['project_id'], 'task_id': self.object.pk})

    # Mettre à jour la méthode get_context_data() pour inclure l'ID du projet
    # def get_context_data(self, **kwargs):
    #    context = super().get_context_data(**kwargs)
    #    context['project'] = ProjectForm()
    #    return context


class TaskListView(ListView):
    model = Task
    template_name = 'project/task_list.html'

    def get_queryset(self):
        return Task.objects.filter(
            assigned_to=self.request.user)

    # ordering = ['-status', '-priority', '-start_date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = self.get_queryset()
        return context

class TaskDetailView(ListView):
    """
    Afficher les details d'une tache
    """
    model = Task
    template_name = 'project/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs['project_id']
        task_id = self.kwargs['task_id']
        task = Task.objects.get(project__id=project_id, id=task_id)
        context['task'] = task
        return context
        # context['comment_form'] = CommentForm()
        # context['comment_list'] = Comment.objects.filter(task_id=self.kwargs['pk'])

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        task_id = self.kwargs['task_id']
        messages.error(self.request, f"Project ID: {project_id}")
        messages.error(self.request, f"Task ID: {task_id}")
        queryset = super().get_queryset()
        return queryset.filter(pk=task_id, project__pk=project_id)

    def success_url(self):
        return reverse('task_detail', kwargs={'project_id': self.object.project.pk, 'pk': self.object.pk})


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'project/task_update.html'
    success_url = reverse_lazy('tasks_list')

    # success_url = reverse_lazy('project_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modifier la tâche'
        context['button_label'] = 'Modifier'
        context['status'] = self.object.get_status_display()
        context['project'] = ProjectForm()
        context['assigned_to_choices'] = User.objects.all()
        return context

    def form_valid(self, form):
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        # Si le formulaire n'est pas valide, renvoyer la page avec le formulaire et les erreurs
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('task_list')
        # return reverse('task_detail', kwargs={'project_id': self.object.project.pk, 'task_id': self.object.pk})


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'project/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def get_success_url(self):
        messages.success(self.request, f"Task {self.object.name} has been deleted successfully")
        return reverse_lazy('task_list', kwargs={'project_id': self.object.project.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.object
        return context


def complete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.status = 'COMPLETED'
    task.save()
    return redirect('task_list')


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


@login_required
def calendar(request):
    projects = Project.objects.filter(assigned_to=request.user).distinct()
    tasks = Task.objects.filter(assigned_to=request.user).distinct()
    events = []
    for task in tasks:
        event = {
            'title': task.name,
            'start': task.start_date,
            'end': task.end_date,
            'url': reverse_lazy('task_detail', kwargs={'pk': task.pk}),
            'color': 'red' if task.status == 'incomplete' else 'green',
        }
        events.append(event)
    return render(request, 'project/calendar.html', {'events': events})


@csrf_exempt
def event_api(request):
    events = []
    for task in Task.objects.all():
        event = {
            'title': task.name,
            'start': task.start_date.isoformat(),
            'end': task.end_date.isoformat(),
            'url': reverse_lazy('task_detail', kwargs={'pk': task.pk}),
            'color': 'red' if task.status == 'incomplete' else 'green',
        }
        events.append(event)

    return JsonResponse(events, safe=False)


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST,
                                   instance=request.user)
        password_form = PasswordChangeForm(request.user,
                                           request.POST)

        if user_form.is_valid() and password_form.is_valid():
            user = user_form.save()
            update_session_auth_hash(request, user)
            password_form.save()
            return redirect('profile')
    else:
        user_form = UserChangeForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)

    context = {
        'user_form': user_form,
        'password_form': password_form,
    }
    return render(request, 'profile.html', context)
