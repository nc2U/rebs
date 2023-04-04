from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import User

from .forms import UserCreationForm


class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')


class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'


def create_superuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        User.objects.create_superuser(username=username,
                                      email=email,
                                      password=password)
        return redirect('home')
    else:
        return render(request, 'setup/create_superuser.html')
