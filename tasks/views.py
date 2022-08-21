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
            Task.objects.create(author=request.user, name=add_task_form.cleaned_data['name'],
                                description=add_task_form.cleaned_data['description'])
            return redirect('home')
        return render(request, 'tasks/add_task.html', {'form': add_task_form})
    return render(request, 'tasks/add_task.html', {'form': add_task_form})


# Create your views here.
