from urllib import request
from django.shortcuts import render
from django.views.generic import ListView, CreateView, FormView
from .forms import RegistrationUserForm, AddTaskForm
from django.urls import reverse_lazy
from .models import Task, Profile
from django.utils.text import slugify
from django.shortcuts import redirect


class MainPage(ListView):
    queryset = Task.objects.all()
    template_name = "tasks/index.html"


class RegisterUser(CreateView):
    form_class = RegistrationUserForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')


class AddTask(FormView):
    template_name = 'tasks/add_task.html'
    success_url = '/main/'
    form_class = AddTaskForm


def add_task(request):
    add_task_form = AddTaskForm(request.POST)
    if request.method == 'POST':
        if add_task_form.is_valid():
            user_profile = Profile.objects.get(user=request.user)
            Task.objects.create(title=add_task_form.cleaned_data['title'], slug=slugify(add_task_form.cleaned_data['title']), profile=user_profile,
                                description=add_task_form.cleaned_data['description'])
            return redirect('profile')
        return render(request, 'tasks/add_task.html', {'form': add_task_form})
    return render(request, 'tasks/add_task.html', {'form': add_task_form})


def mark_as_comleted(request, slug):
    profile = Profile.objects.get(user=request.user)
    task = Task.objects.get(profile=profile, slug=slug)
    task.is_completed = True
    task.save()
    profile.completed_tasks += 1
    profile.save()
    return redirect('profile')


def delete_task(request, slug):
    profile = Profile.objects.get(user=request.user)
    task = Task.objects.get(profile=profile, slug=slug)
    if task.is_completed:
        profile.completed_tasks += 1
        profile.save()
    else:
        profile.uncompleted_tasks += 1
        profile.save()
    task.delete()
    return redirect('profile')


def delete_all_tasks(request):
    profile = Profile.objects.get(user=request.user)
    tasks = Task.objects.filter(profile=profile)
    for task in tasks:
        if task.is_completed:
            profile.completed_tasks += 1
        else:
            profile.uncompleted_tasks += 1
    profile.save()
    tasks.delete()
    return redirect('profile')


def profile(request):
    if Profile.objects.filter(user=request.user):
        profile = Profile.objects.get(user=request.user)
        completed_tasks = Task.objects.filter(profile=profile, is_completed=True)
        uncompleted_tasks = Task.objects.filter(profile=profile, is_completed=False)
        completed_tasks_number = Task.objects.filter(profile=profile, is_completed=True).count()
        uncompleted_tasks_number = Task.objects.filter(profile=profile, is_completed=False).count()
        try:
            value = int(completed_tasks.count() / Task.objects.filter(profile=profile).count()) * 100
        except:
            value = 0
        return render(request, 'tasks/profile.html', {"completed_tasks": completed_tasks, "uncompleted_tasks": uncompleted_tasks,
                                                      "value": value, "completed_tasks_number": completed_tasks_number,
                                                      "uncompleted_tasks_number":uncompleted_tasks_number})
    else:
        Profile.objects.create(user=request.user)
        return render(request, 'tasks/profile.html')
    
# Create your views here.
