from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from .models import User
# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


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


@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})
