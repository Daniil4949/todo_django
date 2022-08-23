from urllib import request
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .forms import RegistrationUserForm, AddTaskForm
from django.urls import reverse_lazy
from .models import Task, Profile
from django.utils.text import slugify
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User


class MainPage(ListView):
    """Main page ListView"""
    queryset = Task.objects.all()
    template_name = "tasks/index.html"


class RegisterUser(CreateView):
    """Register user class"""
    form_class = RegistrationUserForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')


class LoginUser(LoginView):
    """Login user view"""
    template_name = 'registration/login.html'
    model = User
    success_url = reverse_lazy('home')


def add_task(request):
    """add task form. The necessary variables are: title, description.
        Other  variables are not necessary in the form. """
    add_task_form = AddTaskForm(request.POST)
    if request.method == 'POST':
        if add_task_form.is_valid():
            user_profile = Profile.objects.get(user=request.user)
            Task.objects.create(title=add_task_form.cleaned_data['title'],
                                slug=slugify(add_task_form.cleaned_data['title']), profile=user_profile,
                                description=add_task_form.cleaned_data['description'])
            return redirect('profile')
        return render(request, 'tasks/add_task.html', {'form': add_task_form})
    return render(request, 'tasks/add_task.html', {'form': add_task_form})


def mark_as_comleted(request, slug):
    """Mark a user's task as a completed one"""
    profile = Profile.objects.get(user=request.user)
    task = Task.objects.get(profile=profile, slug=slug)
    task.is_completed = True
    task.save()
    profile.completed_tasks += 1
    profile.save()
    return redirect('profile')


def delete_task(request, slug):
    """Deleting user's task"""
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
    """Deleting all the user's tasks"""
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
    """User profile with all the task and the user's progress.
    try/except block is necessary in case of absence of the user's tasks.
    It causes DivisionByZero error"""
    if Profile.objects.filter(user=request.user):
        profile = Profile.objects.get(user=request.user)
        completed_tasks = Task.objects.filter(profile=profile, is_completed=True)
        uncompleted_tasks = Task.objects.filter(profile=profile, is_completed=False)
        completed_tasks_number = Task.objects.filter(profile=profile, is_completed=True).count()
        uncompleted_tasks_number = Task.objects.filter(profile=profile, is_completed=False).count()
        try:
            value = int((len(completed_tasks) / len(Task.objects.filter(profile=profile))) * 100)
        except:
            value = 0
        return render(request, 'tasks/profile.html',
                      {"completed_tasks": completed_tasks, "uncompleted_tasks": uncompleted_tasks,
                       "value": value, "completed_tasks_number": completed_tasks_number,
                       "uncompleted_tasks_number": uncompleted_tasks_number})
    else:
        Profile.objects.create(user=request.user)
        return render(request, 'tasks/profile.html')

# Create your views here.
