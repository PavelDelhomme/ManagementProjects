from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from .models import Project, ProjectFile, TaskFile, Task
from .forms import ProjectForm, ProjectFileForm, TaskForm, TaskFileForm


User = get_user_model()


@method_decorator(login_required, name='dispatch')
class ProjectListView(ListView):
    model = Project
    template_name = 'projects/projects_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        if self.request.user.is_manager:
            return Project.objects.filter(manager=self.request.user)
        else:
            return self.request.user.projects.all()


@method_decorator(login_required, name='dispatch')
class ProjectCreateView(CreateView):
    model = Project
    fields = ['name', 'description', 'deadline']
    template_name = 'projects/project_form.html'

    def form_valid(self, form):
        form.instance.manager = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'


@method_decorator(login_required, name='dispatch')
class ProjectUpdateView(UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['name', 'description', 'deadline']
    template_name = 'projects/project_form.html'

    def test_func(self):
        return self.get_object().manager == self.request.user


@method_decorator(login_required, name='dispatch')
class ProjectDeleteView(UserPassesTestMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('project_list')
    template_name = 'projects/project_confirm_delete.html'

    def test_func(self):
        return self.get_object().manager == self.request.user


@method_decorator(login_required, name='dispatch')
class TaskCreateView(CreateView):
    model = Task
    fields = ['name', 'description', 'deadline']
    template_name = 'projects/task_form.html'

    def form_valid(self, form):
        form.instance.project = Project.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['pk'])
        return context


@method_decorator(login_required, name='dispatch')
class TaskDetailView(DetailView):
    model = Task
    template_name = 'projects/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['project_pk'])
        return context


@method_decorator(login_required, name='dispatch')
class TaskUpdateView(UserPassesTestMixin, UpdateView):
    model = Task
    fields = ['name', 'description', 'deadline']
    template_name = 'projects/task_form.html'

    def test_func(self):
        return self.get_object().project.manager == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project'] = Project.objects.get(pk=self.kwargs['project_pk'])
        return context


@method_decorator(login_required, name='dispatch')
class TaskDeleteView(UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'projects/task_confirm_delete.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('project_detail', kwargs={'pk': self.kwargs['project_pk']})

    def test_func(self):
        return self.get_object().project.manager == self.request.user


@login_required
def projects_list(request):
    """
    Affiche la liste des projets
    """
    user = request.user
    if user.is_manager:
        projects = user.projects_managed.all()
    else:
        projects = user.assigned_projects.all()
    return render(request, 'projects/projects_list.html', {'projects': projects})


@login_required
def project_detail(request, project_id):
    """
    Affiche les détails d'un projet
    """
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    if not (user in project.assigned_users.all() or user.groups.filter(
            id__in=project.assigned_groups.all().values('id'))):
        messages.error(request, "Vous n'avez pas accès à ce projet.")
        return redirect('projects_list')
    tasks = project.tasks.all()
    return render(request, 'projects/project_detail.html', {'project': project, 'tasks': tasks})


@login_required
def project_create(request):
    """
    Créer un nouveau projet
    """
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.manager = request.user
            project.save()
            form.save_m2m()
            messages.success(request, 'Le projet a été créé avec succès.')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm()
    return render(request, 'projects/project_form.html', {'form': form})


@login_required
def project_edit(request, project_id):
    """
    Editer un projet existant
    """
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    if user != project.manager:
        messages.error(request, "Vous n'êtes pas autorisé à éd")


@login_required
def project_delete(request, project_id):
    """
    Supprimer un projet existant
    """
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    if user != project.manager:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer ce projet.")
        return redirect('project_detail', project_id=project.id)
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Le projet a été supprimé avec succès.")
        return redirect('projects_list')
    return render(request, 'projects/project_confirm_delete.html', {'project': project})


@login_required
def task_create(request, project_id):
    """
    Créer une tâche pour un projet
    """
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    if not (user == project.manager or user in project.assigned_users.all() or user.groups.filter(
            id__in=project.assigned_groups.all().values('id'))):
        messages.error(request, "Vous n'êtes pas autorisé à créer une tâche pour ce projet.")
        return redirect('project_detail', project_id=project.id)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            form.save_m2m()
            messages.success(request, 'La tâche a été créée avec succès.')
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm()
    return render(request, 'projects/task_form.html', {'form': form, 'project': project})


@login_required
def task_edit(request, task_id):
    """
    Editer une tâche existante
    """
    task = get_object_or_404(Task, pk=task_id)
    project = task.project
    user = request.user
    if not (user == project.manager or user in project.assigned_users.all() or user.groups.filter(
            id__in=project.assigned_groups.all().values('id'))):
        messages.error(request, "Vous n'êtes pas autorisé à éditer cette tâche.")
        return redirect('project_detail', project_id=project.id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            form.save_m2m()
            messages.success(request, 'La tâche a été éditée avec succès.')
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'projects/task_form.html', {'form': form, 'project': project, 'task': task})


@login_required
def task_delete(request, task_id):
    """
    Supprime une tâche
    """
    task = get_object_or_404(Task, pk=task_id)
    project = task.project
    user = request.user
    if user != task.created_by and user != project.manager:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer cette tâche.")
        return redirect('project_detail', project_id=project.id)
    task.delete()
    messages.success(request, "La tâche a été supprimée avec succès.")
    return redirect('project_detail', project_id=project.id)


@login_required
def project_file_upload(request, project_id):
    """
    Télécharger un fichier pour un projet
    """
    project = get_object_or_404(Project, pk=project_id)
    user = request.user
    if user != project.manager:
        messages.error(request, "Vous n'êtes pas autorisé à télécharger des fichiers pour ce projet.")
        return redirect('project_detail', project_id=project.id)
    if request.method == 'POST':
        form = ProjectFileForm(request.POST, request.FILES)
        if form.is_valid():
            project_file = form.save(commit=False)
            project_file.project = project
            project_file.uploaded_by = user
            project_file.save()
            messages.success(request, 'Le fichier a été téléchargé avec succès.')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectFileForm()
    return render(request, 'projects/project_file_upload.html', {'form': form, 'project': project})


@login_required
def project_file_delete(request, project_file_id):
    """
    Supprime un fichier de projet
    """
    project_file = get_object_or_404(ProjectFile, pk=project_file_id)
    project = project_file.project
    user = request.user
    if user != project.manager:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer ce fichier.")
        return redirect('project_detail', project_id=project.id)
    project_file.delete()
    messages.success(request, "Le fichier a été supprimé avec succès.")
    return redirect('project_detail', project_id=project.id)


@login_required
def task_file_upload(request, task_id):
    """
    Télécharger un fichier pour une tâche
    """
    task = get_object_or_404(Task, pk=task_id)
    project = task.project
    user = request.user
    if user != task.created_by and user != project.manager:
        messages.error(request, "Vous n'êtes pas autorisé à télécharger des fichiers pour cette tâche.")
        return redirect('project_detail', project_id=project.id)
    if request.method == 'POST':
        form = TaskFileForm(request.POST, request.FILES)
        if form.is_valid():
            task_file = form.save(commit=False)
            task_file.task = task
            task_file.uploaded_by = user
            task_file.save()
            messages.success(request, 'Le fichier a été téléchargé avec succès.')
            return redirect('project_detail', project_id=project.id)
    else:
        form = TaskFileForm()
    return render(request, 'projects/task_file_upload.html', {'form': form, 'task': task})


@login_required
def task_file_delete(request, task_file_id):
    """
    Supprime un fichier de tâche
    """
    task_file = get_object_or_404(TaskFile, pk=task_file_id)
    task = task_file.task
    if request.method == 'POST':
        task_file.delete()
        messages.success(request, 'Le fichier a été supprimé avec succès.')
        return redirect('task_detail', task_id=task.id)
    return render(request, 'projects/task_file_delete.html', {'task_file': task_file})
