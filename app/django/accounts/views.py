from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from .models import User
from company.models import Company
from project.models import Project

from .forms import UserCreationForm


class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')


class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html'


def install_check_step(request):
    is_project = Project.objects.all().exists()
    is_company = Company.objects.all().exists()
    is_superuser = User.objects.filter(is_superuser=True).exists()

    if is_project:
        return redirect('/')
    elif not is_superuser:
        return redirect('/install/create/superuser/')
    elif not is_company:
        return redirect('/install/create/company/')
    else:
        return redirect('/install/create/project/')


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
        is_superuser = User.objects.filter(is_superuser=True).exists()
        if is_superuser:
            return redirect('/install/create/company/')
        else:
            return render(request, 'install/create_superuser.html')


def create_company(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        tax_number = request.POST.get('tax_number')
        ceo = request.POST.get('ceo')
        org_number = request.POST.get('org_number')
        Company.objects.create(name=name,
                               tax_number=tax_number,
                               ceo=ceo,
                               org_number=org_number)
        return redirect('/install/create/project/')
    else:
        is_superuser = User.objects.filter(is_superuser=True).exists()
        is_company = Company.objects.all().exists()
        if not is_superuser:
            return redirect('/install/create/superuser/')
        elif is_company:
            return redirect('/install/create/project/')
        else:
            return render(request, 'install/create_company.html')


def data_seeding(request):
    pass


def create_project(request):
    if request.method == 'POST':
        company = request.POST.get('company')
        name = request.POST.get('name')
        kind = request.POST.get('kind')
        start_year = request.POST.get('start_year')
        local_zipcode = request.POST.get('local_zipcode')
        local_address1 = request.POST.get('local_address1')
        local_address2 = request.POST.get('local_address2')
        local_address3 = request.POST.get('local_address3')
        area_usage = request.POST.get('area_usage')
        build_size = request.POST.get('build_size')
        Project.objects.create(company=company,
                               name=name,
                               kind=kind,
                               start_year=start_year,
                               local_zipcode=local_zipcode,
                               local_address1=local_address1,
                               local_address2=local_address2,
                               local_address3=local_address3,
                               area_usage=area_usage,
                               build_size=build_size)

        data_seeding()
        return redirect('/')
    else:
        is_company = Company.objects.all().exists()
        if is_company:
            companies = Company.objects.all()
            return render(request, 'install/create_project.html', {'companies': companies})
        else:
            return redirect('/install/create/company/')
