from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView
from django.views.generic import CreateView, UpdateView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, Http404
from .models import Project, Task, Event
from .forms import ProjectForm, TaskForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


class HomePageView(TemplateView):
    template_name = 'home.html'  # Le template qui va etre affiche dans la page home


class ProjectListView(ListView):
    """
    Lister tous les projets
    """
    model = Project  # Le model sur lequel on va travailler
    template_name = 'project/project_list.html'  # Le template qui va etre affiche dans la page project_list
    ordering = ['-start_date']  # L'ordre dans lequel on va afficher les projets

    def get_queryset(self):  # La methode qui va retourner tous les projets
        """
        Retourne tous les projets
        :return:
        """
        # return Project.objects.all()  # Retourne tous les projets
        return Project.objects.filter(
            assigned_to=self.request.user)  # Retourne tous les projets assignes a l'utilisateur connecte


class ProjectCreateView(CreateView):
    """
    Creer un nouveau projet
    """
    model = Project  # Le model sur lequel on va travailler
    template_name = 'project/project_create.html'  # Le template qui va etre affiche dans la page project_create
    fields = ['name', 'description', 'assigned_to', 'start_date',
              'end_date']  # Les champs du model sur lesquels on va travailler
    success_url = reverse_lazy(
        'project_list_by_start_date')  # La page sur laquelle on va etre redirige apres la creation du projet

    def form_valid(self, form):
        """
        Methode qui va permettre de creer un nouveau projet
        :param form:
        :return:
        """
        form.instance.created_by = self.request.user  # On recupere l'utilisateur connecte
        return super().form_valid(form)  # On retourne la methode form_valid de la classe CreateView

    def get_success_url(self):
        """
        Methode qui va permettre de rediriger l'utilisateur apres la creation du projet
        :return:
        """
        return reverse_lazy('project_detail', kwargs={'pk': self.object.pk})  # On retourne la page project_detail


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
    """
    Creer une nouvelle tache
    """
    model = Task  # Le model sur lequel on va travailler
    form_class = TaskForm  # Le formulaire sur lequel on va travailler
    template_name = 'project/task_create.html'  # Le template qui va etre affiche dans la page task_create
    success_url = reverse_lazy('project_list')  # La page sur laquelle on va etre redirige apres la creation de la tache

    # def get_initial(self):
    #    project = get_object_or_404(Project, pk=self.kwargs['project_id'])
    #    return {'project': project}

    def form_valid(self, form):
        """
        Methode qui va permettre de creer une nouvelle tache
        :param form:
        :return:
        """
        project = get_object_or_404(Project,
                                    id=self.kwargs['project_id'])  # On recupere le projet sur lequel on va travailler
        form.instance.created_by = self.request.user  # On recupere l'utilisateur connecte
        # form.instance.project_id = get_object_or_404(Project, pk=self.kwargs['project_id']) # On recupere le projet sur lequel on va travailler
        form.instance.project = project  # On recupere le projet sur lequel on va travailler
        print(form.instance.project)  # <Project: Project 1> # On affiche le projet sur lequel on va travailler
        return super().form_valid(form)  # On retourne la methode form_valid de la classe CreateView

    def get_context_data(self, **kwargs):
        """
        Methode qui va permettre de recuperer le projet sur lequel on va travailler
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)  # On recupere le contexte
        context['project'] = ProjectForm()  # On recupere le projet sur lequel on va travailler
        return context  # On retourne le contexte


class TaskListView(ListView):
    """
    Lister toutes les taches
    """
    model = Task  # Le model sur lequel on va travailler
    template_name = 'project/task_list.html'  # Le template qui va etre affiche dans la page task_list
    # ordering = ['-start_date'] # L'ordre dans lequel on va afficher les taches
    ordering = ['-status', '-priority', '-start_date']  # L'ordre dans lequel on va afficher les taches

    def get_queryset(self):
        """
        Retourne toutes les taches assignees a l'utilisateur connecte
        :return:
        """
        return Task.objects.filter(
            assigned_to=self.request.user)  # Retourne toutes les taches assignees a l'utilisateur connecte


class TaskDetailView(ListView):
    """
    Afficher les details d'une tache
    """
    model = Task  # Le model sur lequel on va travailler
    template_name = 'project/task_detail.html'  # Le template qui va etre affiche dans la page task_detail

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        task_id = self.kwargs['task_id']
        messages.error(self.request, f"Project ID: {project_id}")
        messages.error(self.request, f"Task ID: {task_id}")
        queryset = super().get_queryset()
        return queryset.filter(pk=task_id, project__pk=project_id)


class TaskUpdateView(UpdateView):
    """
    Mettre a jour une tache
    """
    model = Task  # Le model sur lequel on va travailler
    form_class = TaskForm  # Le formulaire sur lequel on va travailler
    template_name = 'project/task_update.html'  # Le template qui va etre affiche dans la page task_update

    # success_url = reverse_lazy('project_list')

    def get_context_data(self, **kwargs):
        """
        Methode qui va permettre de recuperer le projet sur lequel on va travailler
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)  # On recupere le contexte
        context['project'] = ProjectForm()  # On recupere le projet sur lequel on va travailler
        return context  # On retourne le contexte

    def form_valid(self, form):
        """
        Methode qui va permettre de mettre a jour une tache
        :param form:
        :return:
        """
        form.instance.modified_by = self.request.user  # On recupere l'utilisateur connecte
        return super().form_valid(form)  # On retourne la methode form_valid de la classe UpdateView

    def get_success_url(self):
        """
        Methode qui va permettre de rediriger l'utilisateur apres la mise a jour de la tache
        :return:
        """
        return reverse('task_detail', kwargs={'project_id': self.object.project.pk, 'task_id': self.object.pk})


class TaskDeleteView(DeleteView):
    """
    Supprimer une tache
    """
    model = Task
    template_name = 'project/task_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('task_list', kwargs={'project_id': self.object.project.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.object
        return context
    # success_url = reverse_lazy('task_list') # La page sur laquelle on va etre redirige apres la suppression de la
    # tache


@login_required  # On demande a l'utilisateur d'etre connecte
def add_task_comment(request, pk):
    """
    Ajouter un commentaire a une tache
    :param request:
    :param pk:
    :return:
    """
    task = get_object_or_404(Task, pk=pk)  # On recupere la tache sur laquelle on va travailler
    if request.method == 'POST':  # Si la methode est POST
        task.comments = request.POST['comments']  # On recupere les commentaires
        task.save()  # On sauvegarde les commentaires
    context = {
        'task': task,  # On recupere la tache sur laquelle on va travailler
    }
    return render(request, 'project/task_detail.html',
                  context)  # On retourne le template task_detail.html avec le contexte


class SignUpView(CreateView):
    """
    Inscription d'un utilisateur
    """
    form_class = UserCreationForm  # Le formulaire sur lequel on va travailler
    success_url = reverse_lazy('login')  # La page de redirection apres l'inscription
    template_name = 'signup.html'  # Le template qui va etre affiche dans la page signup


@login_required
def all_notifications(request):
    """
    Afficher toutes les notifications
    :param request:
    :return:
    """
    return render(request, 'all_notifications.html')


def project_detail(request, pk):
    """
    Afficher les details d'un projet
    :param request:
    :param pk:
    :return:
    """
    project = get_object_or_404(Project, pk=pk)  # On recupere le projet sur lequel on va travailler
    tasks = Task.objects.filter(project=project)  # On recupere toutes les taches du projet
    context = {
        'project': project,
        'tasks': tasks,
    }
    return render(request, 'project/project_detail.html', context)


@login_required
def calendar(request):
    """
    Show calendar
    """
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
    """
    Afficher le profil de l'utilisateur
    :param request:
    :return:
    """
    if request.method == 'POST':  # Si la methode est POST
        user_form = UserChangeForm(request.POST,
                                   instance=request.user)  # On recupere le formulaire de modification de l'utilisateur
        password_form = PasswordChangeForm(request.user,
                                           request.POST)  # On recupere le formulaire de modification du mot de passe

        if user_form.is_valid() and password_form.is_valid():  # Si les deux formulaires sont valides
            user = user_form.save()  # On sauvegarde les modifications de l'utilisateur
            update_session_auth_hash(request, user)  # On met a jour la session
            password_form.save()  # On sauvegarde les modifications du mot de passe
            return redirect('profile')  # On redirige vers la page profile
    else:  # Sinon on affiche le formulaire de modification de l'utilisateur et le formulaire de modification du mot de passe vide
        user_form = UserChangeForm(instance=request.user)  # On recupere le formulaire de modification de l'utilisateur
        password_form = PasswordChangeForm(request.user)  # On recupere le formulaire de modification du mot de passe

    context = {  # On recupere le contexte
        'user_form': user_form,  # On recupere le formulaire de modification de l'utilisateur
        'password_form': password_form,  # On recupere le formulaire de modification du mot de passe
    }
    return render(request, 'profile.html', context)  # On retourne le template profile.html avec le contexte
