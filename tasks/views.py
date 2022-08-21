from django.shortcuts import render
from django.views.generic import ListView, CreateView, FormView
from .forms import RegistrationUserForm, AddTaskForm
from django.urls import reverse_lazy
from .models import Task
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
            Task.objects.create(title=add_task_form.cleaned_data['title'], slug=slugify(add_task_form.cleaned_data['title']))
            return redirect('home')
        return render(request, 'tasks/add_task.html', {'form': add_task_form})
    return render(request, 'tasks/add_task.html', {'form': add_task_form})


def profile(request, user):
    tasks = Task.objects.all()
    return render(request, 'tasks/profile.html', {"tasks": tasks})

# Create your views here.
