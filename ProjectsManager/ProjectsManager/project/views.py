from datetime import datetime

from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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
from django.db.models import Q

from django.contrib.auth import get_user_model
from .models import time_remaining
from .serializer import TaskSerializer

User = get_user_model()


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


class HomePageView(TemplateView):
    template_name = 'home.html'  # Le template qui va etre affiche dans la page home

    def get_context_data(self, **kwargs):
        # On recupere le contexte de la page home et on le stocke dans la variable context
        context = super().get_context_data(**kwargs)
        # On recupere tous les projets et on les stocke dans la variable context sous le nom de projects
        context['projects'] = Project.objects.all()
        # On recupere toutes les taches et on les stocke dans la variable context sous le nom de tasks
        context['tasks'] = Task.objects.all()
        # On recupere toutes les taches dont la date de fin est egale a la date du jour et on les stocke dans la
        # variable context sous le nom de task_due_today
        context['task_due_today'] = Task.objects.filter(end_date=timezone.now().date())
        # On recupere toutes les taches dont la date de fin est inferieure a la date du jour et on les stocke dans la
        # variable context sous le nom de task_overdue
        context['task_overdue'] = Task.objects.filter(end_date__lt=timezone.now().date())
        # On recupere toutes les taches dont le status est complete et on les stocke dans la variable context sous le
        # nom de completed_tasks
        context['completed_tasks'] = Task.objects.filter(status='complete')
        return context  # On retourne le contexte


class ProjectListView(ListView):
    model = Project  # Le model qui va etre utilise
    template_name = 'project/project_list.html'  # Le template qui va etre affiche dans la page project_list
    context_object_name = 'projects'  # Le nom du contexte qui va etre utilise dans le template
    ordering = ['-start_date']  # L'ordre dans lequel les projets vont etre affiches

    def get_queryset(self):
        projects = Project.objects.filter(  # On recupere tous les projets
            assigned_to=self.request.user)  # dont l'utilisateur connecte est assigne a ce projet et on les stocke dans
        # la variable projects
        return projects  # On retourne les projets


class ProjectCreateView(CreateView):
    """
    Création d'un nouveau projet. L'utilisateur qui créé le projet est automatiquement assigné comme le manager de
    projet

    """
    model = Project  # Le model qui va etre utilise pour creer le projet
    template_name = 'project/project_create.html'  # Le template qui va etre affiche dans la page project_create
    fields = ['name', 'description', 'assigned_to', 'start_date',
              # Les champs qui vont etre affiches dans le formulaire de creation de projet
              'end_date']
    success_url = reverse_lazy('project_list_by_start_date')  # L'url de redirection apres la creation du projet

    def form_valid(self, form):
        """
        Ajout de l'utilisateur qui a cree le projet comme manager de projet du projet cree
        :param form:
        :return:
        """
        form.instance.created_by = self.request.user  # On ajoute l'utilisateur qui a cree le projet comme manager de
        # projet du projet cree
        response = super().form_valid(form)  # On appelle la methode form_valid de la classe parente
        return response

    def get_success_url(self):
        return reverse_lazy('project_detail',
                            kwargs={'pk': self.object.pk})  # L'url de redirection apres la creation du projet


class ProjectUpdateView(UpdateView):
    """
    Mise a jour d'un projet existant
    """
    model = Project
    fields = ['name', 'description', 'assigned_to', 'start_date', 'end_date',
              'comments']  # Les champs qui vont etre affiches dans le formulaire de mise a jour de projet
    template_name = 'project/project_update.html'  # Le template qui va etre affiche dans la page project_update
    success_url = reverse_lazy('project_list_by_start_date')  # L'url de redirection apres la mise a jour du projet

    def form_valid(self, form):
        form.instance.updated_by = self.request.user  # On ajoute l'utilisateur qui a mis a jour le projet comme manager
        # de projet du projet mis a jour
        return super().form_valid(form)  # On appelle la methode form_valid de la classe parente


class ProjectDeleteView(DeleteView):
    """
    Suppression d'un projet existant
    """
    model = Project
    template_name = 'project/project_delete.html'  # Le template qui va etre affiche dans la page project_delete
    success_url = reverse_lazy('project_list_by_start_date')  # L'url de redirection apres la suppression du projet

    def delete(self, request, *args, **kwargs):
        """
        Ajout d'un message de succes apres la suppression d'un projet
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        messages.success(request,
                         'Le projet a été supprimé avec succès.')  # On ajoute un message de succes apres la suppression
        # d'un projet
        return super().delete(request, *args, **kwargs)  # On appelle la methode delete de la classe parente

    def get_context_object_name(self, queryset=None):
        """
        Recuperation du nom du contexte qui va etre utilise dans le template
        :param queryset:
        :return:
        """
        obj = super().get_oject(queryset=queryset)  # On recupere l'objet qui va etre supprime
        if not obj.can_be_deleted_by(
                self.request.user):  # Si l'utilisateur connecte n'a pas le droit de supprimer le projet
            raise Http404  # On leve une exception 404
        return obj  # On retourne l'objet


class TaskCreateView(CreateView):
    """
    Creation d'une nouvelle tache
    """
    model = Task
    fields = ['name', 'description', 'assigned_to', 'start_date', 'end_date', 'status',
              'comments']  # Les champs qui vont etre affiches dans le formulaire de creation de tache
    template_name = 'project/task_create.html'  # Le template qui va etre affiche dans la page task_create
    success_url = reverse_lazy('task_list')  # L'url de redirection apres la creation de la tache

    def get(self, request, *args, **kwargs):
        """
        Recuperation du formulaire de creation de tache
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return super().get(request, *args, **kwargs)  # On appelle la methode get de la classe parente

    def post(self, request, *args, **kwargs):
        """
        Traitement du formulaire de creation de tache
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        form = self.get_form()  # On recupere le formulaire de creation de tache
        if form.is_valid():  # Si le formulaire est valide
            return self.form_valid(form)  # On appelle la methode form_valid
        else:  # Sinon
            return self.form_invalid(form)  # On appelle la methode form_invalid

    def form_valid(self, form):
        """
        Ajout de l'utilisateur qui a cree la tache comme manager de tache de la tache creee
        :param form:
        :return:
        """
        form.instance.project_id = self.kwargs['project_id']  # On ajoute l'id du projet auquel la tache est associee
        form.instance.created_by = self.request.user  # On ajoute l'utilisateur qui a cree la tache comme manager de
        # tache de la tache creee
        form.instance.modified_by = self.request.user  # On ajoute l'utilisateur qui a cree la tache comme manager de
        # tache de la tache creee
        response = super().form_valid(form)  # On appelle la methode form_valid de la classe parente
        return response  # On retourne la reponse

    def get_success_url(self):
        """
        L'url de redirection apres la creation de la tache
        :return:
        """
        return reverse_lazy('project_detail', kwargs={
            'pk': self.kwargs['project_id']})  # L'url de redirection apres la creation de la tache

    def get_context_data(self, **kwargs):
        """
        Recuperation du contexte qui va etre utilise dans le template
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)  # On recupere le contexte qui va etre utilise dans le template
        context['project'] = get_object_or_404(Project, pk=self.kwargs[
            'project_id'])  # On ajoute le projet auquel la tache est associee au contexte
        return context  # On retourne le contexte


class TaskListView(LoginRequiredMixin, ListView):
    """
    Liste des taches d'un projet
    """
    model = Task
    context_object_name = 'tasks'
    template_name = 'project/task_list.html'
    paginate_by = 10  # Nombre de taches par page

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')  # On recupere l'id du projet auquel la tache est associee
        completed = self.request.GET.get('completed',
                                         None) == 'True'  # On recupere la valeur du parametre completed de l'url
        if completed == 'True':  # Si completed est egal a True
            return Task.objects.filter(project_id=project_id,
                                       status="completed")  # On retourne les taches du projet dont le status est compl-
            # eted
        elif completed == 'False':  # Si completed est egal a False
            return Task.objects.filter(project_id=project_id,
                                       status='incompleted')  # On retourne les taches du projet dont le status est
            # incompleted
        else:  # Sinon
            return Task.objects.filter(project_id=project_id)  # On retourne toutes les taches du projet

    def get_context_data(self, **kwargs):
        """
        Recuperation du contexte qui va etre utilise dans le template
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)  # On recupere le contexte qui va etre utilise dans le template
        tasks = Task.objects.filter(assigned_to=self.request.user, status="Complete", end_date__lte=datetime.today())
        # On recupere les taches dont le status est complete et dont la date de fin est inferieure ou egale a la date du
        # jour
        context['tasks'] = self.get_queryset()  # On ajoute les taches au contexte
        today = timezone.now().date()  # On recupere la date du jour
        for task in tasks:
            task.time_remaining = time_remaining(task.end_date)  # On calcule le temps restant pour chaque tache
        context['tasks_today'] = Task.objects.filter(assigned_to=self.request.user, end_date=today).order_by(
            'priority')  # On ajoute les taches dont la date de fin est egale a la date du jour au contexte
        context['tasks_later'] = Task.objects.filter(assigned_to=self.request.user, end_date__gt=today).order_by(
            'end_date')  # On ajoute les taches dont la date de fin est superieure a la date du jour au contexte
        context['completed_tasks'] = Task.objects.filter(assigned_to=self.request.user, status="Complete").order_by(
            '-end_date')  # On ajoute les taches dont le status est complete au contexte
        context['tasks_no_due_date'] = Task.objects.filter(assigned_to=self.request.user, end_date=None).order_by(
            'priority')  # On ajoute les taches dont la date de fin est nulle au contexte
        return context  # On retourne le contexte


class TaskDetailView(ListView):
    """
    Afficher les details d'une tache
    """
    model = Task
    template_name = 'project/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs['project_id']  # On recupere l'id du projet auquel la tache est associee
        task_id = self.kwargs['task_id']  # On recupere l'id de la tache
        task = Task.objects.get(project__id=project_id, id=task_id)  # On recupere la tache
        t_remaining = time_remaining(task.date_fin_prevue)  # On calcule le temps restant pour la tache
        print(f"temps restant de la tâche : {t_remaining}")  # On affiche le temps restant
        context = {'task': task, 'time_remaining': t_remaining}  # On ajoute la tache et le temps restant au contexte
        return context  # On retourne le contexte

    def get_queryset(self):
        """
        Recuperation des taches du projet dont l'id est egal a l'id du projet passe en parametre
        :return:
        """
        project_id = self.kwargs['project_id']  # On recupere l'id du projet auquel la tache est associee
        task_id = self.kwargs['task_id']  # On recupere l'id de la tache
        messages.error(self.request, f"Project ID: {project_id}")  # On affiche un message d'erreur
        messages.error(self.request, f"Task ID: {task_id}")  # On affiche un message d'erreur
        queryset = super().get_queryset()  # On recupere les taches du projet
        return queryset.filter(pk=task_id,
                               project__pk=project_id)  # On retourne les taches du projet dont l'id est egal a l'id du
        # projet passe en parametre

    def success_url(self):
        """
        Redirection vers la page de la tache apres la modification
        :return:
        """
        return reverse('task_detail', kwargs={'project_id': self.object.project.pk, 'pk': self.object.pk,
                                              'time_remaining': time_remaining})
        # On retourne l'url de la page de la tache apres la modification avec l'id du projet et l'id de la tache en
        # parametre et le temps restant de la tache en parametre


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'project/task_update.html'
    success_url = reverse_lazy('tasks_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modifier la tâche' # On ajoute le titre au contexte
        context['button_label'] = 'Modifier' # On ajoute le label du bouton au contexte
        context['status'] = self.object.get_status_display() # On ajoute le status de la tache au contexte
        context['project'] = ProjectForm() # On ajoute le formulaire du projet au contexte
        context['assigned_to_choices'] = User.objects.all() # On ajoute les utilisateurs au contexte
        context['time_remaining'] = self.object.time_remaining # On ajoute le temps restant de la tache au contexte
        return context

    def form_valid(self, form):
        form.instance.modified_by = self.request.user # On ajoute l'utilisateur qui a modifie la tache au contexte
        return super().form_valid(form) # On retourne le formulaire valide

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form)) # On retourne le formulaire invalide

    def get_success_url(self):
        return reverse('task_list') # On retourne l'url de la page de la liste des taches

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs() # On recupere les arguments du formulaire
        kwargs['project_id'] = self.get_object().project.id # On ajoute l'id du projet au contexte
        return kwargs


class MarkTaskAsCompletedView(LoginRequiredMixin, View):
    def post(self, request, project_id, task_id, *args, **kwargs):
        """
        Marquer une tache comme terminee
        :param request:
        :param project_id:
        :param task_id:
        :param args:
        :param kwargs:
        :return:
        """
        task = get_object_or_404(Task, pk=task_id) # On recupere la tache dont l'id est egal a l'id de la tache passe en
        # parametre
        task.status = 'complete' # On modifie le status de la tache
        task.date_fin_reelle = timezone.now() # On modifie la date de fin reelle de la tache
        if task.date_debut_prevue: # Si la date de debut prevue de la tache n'est pas vide
            task.temps_reel = (task.date_fin_reelle - task.date_debut_prevue).days * 8 # On calcule le temps reel de la
            # tache
        else: # Sinon
            task.temps_reel = None # On met le temps reel de la tache a vide
        task.temps_passe_reel = task.temps_reel # On met le temps passe reel de la tache a egal au temps reel de la
        # tache
        task.temps_restant_reel = 0 # On met le temps restant reel de la tache a 0
        task.avancement_reel = 100 # On met l'avancement reel de la tache a 100
        task.save() # On sauvegarde la tache
        messages.success(request, "La tâche a été marquée comme terminée.") # On affiche un message de succes
        return HttpResponseRedirect(self.get_redirect_url(project_id=project_id)) # On retourne la redirection vers la
        # page de la tache

    def get_redirect_url(self, *args, **kwargs):
        """
        Redirection vers la page de la tache
        :param args:
        :param kwargs:
        :return:
        """
        project_id = kwargs['project_id'] # On recupere l'id du projet auquel la tache est associee
        # return reverse_lazy('project_detail', args=[project_id])
        return f"{reverse('task_list')}?completed=True&project_id={project_id}" # On retourne l'url de la page de la
        # liste des taches avec le parametre completed a True et l'id du projet en parametre


class MarkTaskAsIncompleteView(LoginRequiredMixin, RedirectView):
    def post(self, request, *args, **kwargs):
        """
        Marquer une tache comme non terminee
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        task = get_object_or_404(Task, pk=kwargs['task_id'])
        task.status = 'incomplete'
        task.save()
        messages.success(request, "La tâche a été marquée comme non terminée.")
        return super().post(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        project_id = kwargs['project_id']
        return reverse_lazy('project_detail', args=[project_id])


class TaskDeleteView(DeleteView):
    """
    Supprimer une tache
    """
    model = Task
    template_name = 'project/task_confirm_delete.html'
    context_object_name = 'task' # On ajoute la tache au contexte

    # success_url = reverse_lazy('task_list')

    def get_success_url(self):
        """
        Redirection vers la page de la liste des taches
        :return:
        """
        messages.success(self.request, f"Task {self.object.name} has been deleted successfully") # On affiche un message
        project_id = self.object.project.id # On recupere l'id du projet auquel la tache est associee
        return reverse_lazy('task_list', kwargs={'project_id': project_id}) # On retourne l'url de la page de la liste

    def get_context_data(self, **kwargs):
        """
        Ajouter la tache au contexte
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs) # On recupere le contexte du formulaire de suppression de la tache
        context['task'] = self.object # On ajoute la tache au contexte du formulaire de suppression de la tache
        return context # On retourne le contexte


# def complete_task(request, pk):
#    task = get_object_or_404(Task, pk=pk)
#    task.status = 'COMPLETED'
#    task.save()
#    return redirect('task_list')

class ProjectDetailView(DetailView):
    """
    Afficher les details d'un projet
    """
    model = Project
    template_name = 'project/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project_id = self.kwargs['pk']
        context['project'] = Project.objects.get(id=project_id)
        context['tasks'] = Task.objects.filter(project=project_id)
        return context


class SignUpView(CreateView):
    """
    Inscription d'un utilisateur
    """
    form_class = UserCreationForm # On utilise le formulaire de creation d'un utilisateur de Django
    success_url = reverse_lazy('login') # On redirige vers la page de connexion
    template_name = 'signup.html' # On utilise le template signup.html


@login_required # On demande a l'utilisateur d'etre connecte pour acceder a cette page
def add_task_comment(request, pk):
    task = get_object_or_404(Task, pk=pk) # On recupere la tache
    if request.method == 'POST': # Si la methode de la requete est POST
        task.comments = request.POST['comments'] # On recupere les commentaires de la tache
        task.save() # On sauvegarde la tache
    context = { # On ajoute la tache au contexte
        'task': task,
    }
    return render(request, 'project/task_detail.html', context) # On retourne la page de la tache


@login_required # On demande a l'utilisateur d'etre connecte pour acceder a cette page
def calendar(request):
    projects = Project.objects.filter(assigned_to=request.user).distinct() # On recupere les projets de l'utilisateur
    tasks = Task.objects.filter(assigned_to=request.user).distinct() # On recupere les taches de l'utilisateur
    events = [] # On initialise la liste des evenements
    for task in tasks: # Pour chaque tache
        event = { # On ajoute un evenement
            'title': task.name, # Le titre de l'evenement est le nom de la tache
            'start': task.start_date, # La date de debut de l'evenement est la date de debut de la tache
            'end': task.end_date, # La date de fin de l'evenement est la date de fin de la tache
            'url': reverse_lazy('task_detail', kwargs={'pk': task.pk}), # L'url de l'evenement est l'url de la page de la tache
            'color': 'red' if task.status == 'incomplete' else 'green', # La couleur de l'evenement est rouge si la tache est incomplete et verte si la tache est complete
        }
        events.append(event) # On ajoute l'evenement a la liste des evenements
    return render(request, 'project/calendar.html', {'events': events}) # On retourne la page du calendrier avec la liste des evenements


@csrf_exempt # On desactive la protection CSRF
def event_api(request): # On cree une vue pour l'API des evenements
    events = [] # On initialise la liste des evenements
    for task in Task.objects.all(): # Pour chaque tache
        event = { # On ajoute un evenement
            'title': task.name, # Le titre de l'evenement est le nom de la tache
            'start': task.start_date.isoformat(), # La date de debut de l'evenement est la date de debut de la tache
            'end': task.end_date.isoformat(), # La date de fin de l'evenement est la date de fin de la tache
            'url': reverse_lazy('task_detail', kwargs={'pk': task.pk}), # L'url de l'evenement est l'url de la page de la tache
            'color': 'red' if task.status == 'incomplete' else 'green', # La couleur de l'evenement est rouge si la tache est incomplete et verte si la tache est complete
        }
        events.append(event) # On ajoute l'evenement a la liste des evenements

    return JsonResponse(events, safe=False) # On retourne la liste des evenements au format JSON


@login_required
def profile(request): # On cree une vue pour la page de profil
    if request.method == 'POST': # Si la methode de la requete est POST
        user_form = UserChangeForm(request.POST,
                                   instance=request.user) # On utilise le formulaire de modification d'un utilisateur
        password_form = PasswordChangeForm(request.user,
                                           request.POST) # On utilise le formulaire de modification du mot de passe

        if user_form.is_valid() and password_form.is_valid(): # Si les deux formulaires sont valides
            user = user_form.save() # On sauvegarde les donnees du formulaire
            update_session_auth_hash(request, user) # On met a jour la session
            password_form.save() # On sauvegarde le mot de passe
            return redirect('profile') # On redirige vers la page de profil
    else: # Si la methode de la requete est GET
        user_form = UserChangeForm(instance=request.user) # On utilise le formulaire de modification d'un utilisateur
        password_form = PasswordChangeForm(request.user) # On utilise le formulaire de modification du mot de passe

    context = { # On ajoute les formulaires au contexte
        'user_form': user_form,
        'password_form': password_form,
    }
    return render(request, 'profile.html', context) # On retourne la page de profil


class ProjectSearchView(ListView):
    """
    Recherche de projets et de taches
    """
    model = Project
    template_name = 'project/project_search_result.html'
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q') # On recupere la recherche
        if query: # Si la recherche n'est pas vide
            project_results = Project.objects.filter(Q(name__icontains=query) | Q(description__icontains=query),
                                                     assigned_to=self.request.user) # On recupere les projets qui correspondent a la recherche
            task_results = Task.objects.filter(Q(name__icontains=query) | Q(description__icontains=query),
                                               assigned_to=self.request.user) # On recupere les taches qui correspondent a la recherche
            return list(project_results) + list(task_results) # On retourne la liste des projets et des taches
        return [] # On retourne une liste vide


# Implémentation du calendrier
@method_decorator(login_required, name='dispatch')
class TaskListAPIView(View):
    """
    API pour la liste des taches au format JSON pour le calendrier
    """
    def get(self, request):
        tasks = Task.objects.all() # On recupere toutes les taches
        serializer = TaskSerializer(tasks, many=True) # On serialise les taches
        events = [] # On initialise la liste des evenements
        for task in tasks:
            event = { # On ajoute un evenement
                'id': task.id, # L'id de l'evenement est l'id de la tache
                'title': task.title, # Le titre de l'evenement est le titre de la tache
                'start': task.start_date.isoformat(), # La date de debut de l'evenement est la date de debut de la tache
                'end': task.end_date.isoformat(), # La date de fin de l'evenement est la date de fin de la tache
                'description': task.description, # La description de l'evenement est la description de la tache
                'backgroundColor': 'red' if task.status == 'incomplete' else 'green',   # La couleur de l'evenement est rouge si la tache est incomplete et verte si la tache est complete
                # 'url': '/task_detail/' + str(task.id), # L'url de l'evenement est l'url de la page de la tache
            }
            events.append(event) # On ajoute l'evenement a la liste des evenements
        return JsonResponse(events, safe=False) # On retourne la liste des evenements au format JSON
