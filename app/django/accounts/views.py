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


def superuser_check(request):
    is_superuser = User.objects.filter(is_superuser=True).exists()

    if is_superuser:
        return redirect('/')
    else:
        return redirect('/install/create/superuser/')


def create_superuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        User.objects.create_superuser(username=username,
                                      email=email,
                                      password=password)
        return redirect('/install/create/company/')
    else:
        return render(request, 'install/create_superuser.html')


def create_company(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        User.objects.create_superuser(username=username,
                                      email=email,
                                      password=password)
        return redirect('/')
    else:
        return render(request, 'install/create_company.html')
