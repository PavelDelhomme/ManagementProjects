from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from .models import User
# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        user = form.save()
        user.birth_date = form.cleaned_data.get('birth_date')
        user.is_manager = form.cleaned_data.get('is_manager')
        user.save()
        return redirect('login')


class LoginView(LoginView):
    template_name = 'login.html'


class LogoutView(LogoutView):
    template_name = 'logout.html'


login = LoginView.as_view()


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'accounts.profile.html'


#@login_required
#def profile(request):
#    return render(request, 'accounts/profile.html', {'user': request.user})
