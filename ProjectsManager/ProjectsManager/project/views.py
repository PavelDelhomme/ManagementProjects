from datetime import datetime

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic.edit import DeleteView, FormMixin
from django.views.generic import CreateView, UpdateView, DetailView, RedirectView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, Http404, HttpResponseRedirect
from .models import Project, Task, Event, time_remaining
from .forms import ProjectForm, TaskForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from django.contrib.auth import get_user_model
from .models import time_remaining

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


class TaskCreateView(CreateView):
    model = Task
    fields = ['name', 'description', 'assigned_to', 'start_date', 'end_date', 'status', 'comments']
    template_name = 'project/task_create.html'
    success_url = reverse_lazy('task_list')

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.project_id = self.kwargs['project_id']
        form.instance.created_by = self.request.user
        form.instance.modified_by = self.request.user
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('project_detail', kwargs={'pk': self.object.project_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = get_object_or_404(Project, pk=self.kwargs['project_id'])
        return context


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'project/task_list.html'
    paginate_by = 10

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        completed = self.request.GET.get('completed', None) == 'True'
        if completed == 'True':
            return Task.objects.filter(project_id=project_id, status="completed")
        elif completed == 'False':
            return Task.objects.filter(project_id=project_id, status='incompleted')
        else:
            return Task.objects.filter(project_id=project_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tasks = Task.objects.filter(assigned_to=self.request.user, status="Complete", end_date__lte=datetime.today())
        context['tasks'] = self.get_queryset()
        today = timezone.now().date()
        for task in tasks:
            task.time_remaining = time_remaining(task.end_date)
        context['tasks_today'] = Task.objects.filter(assigned_to=self.request.user, end_date=today).order_by('priority')
        context['tasks_later'] = Task.objects.filter(assigned_to=self.request.user, end_date__gt=today).order_by(
            'end_date')
        context['completed_tasks'] = Task.objects.filter(assigned_to=self.request.user, status="Complete").order_by(
            '-end_date')
        context['tasks_no_due_date'] = Task.objects.filter(assigned_to=self.request.user, end_date=None).order_by(
            'priority')
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
        t_remaining = time_remaining(task.date_fin_prevue)
        print(f"temps restant de la tâche : {t_remaining}")
        context = {'task': task, 'time_remaining': t_remaining}
        return context

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        task_id = self.kwargs['task_id']
        messages.error(self.request, f"Project ID: {project_id}")
        messages.error(self.request, f"Task ID: {task_id}")
        queryset = super().get_queryset()
        return queryset.filter(pk=task_id, project__pk=project_id)

    def success_url(self):
        return reverse('task_detail', kwargs={'project_id': self.object.project.pk, 'pk': self.object.pk,
                                              'time_remaining': time_remaining})


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'project/task_update.html'
    success_url = reverse_lazy('tasks_list')

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
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('task_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['project_id'] = self.get_object().project.id
        return kwargs


class MarkTaskAsCompletedView(LoginRequiredMixin, View):
    def post(self, request, project_id, task_id, *args, **kwargs):
        task = get_object_or_404(Task, pk=task_id)
        task.status = 'complete'
        task.date_fin_reelle = timezone.now()
        if task.date_debut_prevue:
            task.temps_reel = (task.date_fin_reelle - task.date_debut_prevue).days * 8
        else:
            task.temps_reel = None
        task.temps_passe_reel = task.temps_reel
        task.temps_restant_reel = 0
        task.avancement_reel = 100
        task.save()
        messages.success(request, "La tâche a été marquée comme terminée.")
        return HttpResponseRedirect(self.get_redirect_url(project_id=project_id))

    def get_redirect_url(self, *args, **kwargs):
        project_id = kwargs['project_id']
        # return reverse_lazy('project_detail', args=[project_id])
        return f"{reverse('task_list')}?completed=True&project_id={project_id}"


class MarkTaskAsIncompleteView(LoginRequiredMixin, RedirectView):
    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['task_id'])
        task.status = 'incomplete'
        task.save()
        messages.success(request, "La tâche a été marquée comme non terminée.")
        return super().post(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        project_id = kwargs['project_id']
        return reverse_lazy('project_detail', args=[project_id])


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


# def complete_task(request, pk):
#    task = get_object_or_404(Task, pk=pk)
#    task.status = 'COMPLETED'
#    task.save()
#    return redirect('task_list')

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs['pk']
        context['project'] = Project.objects.get(id=project_id)
        context['tasks'] = Task.objects.filter(project=project_id)
        return context


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


@login_required
def all_notifications(request):
    return render(request, 'all_notifications.html')


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
