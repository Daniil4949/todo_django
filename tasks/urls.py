from django.urls import path, include
from .views import RegisterUser, MainPage, AddTask, add_task

urlpatterns = [
    path('main/', MainPage.as_view(), name='home'),
    path('accounts/registration/', RegisterUser.as_view(), name='registration'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("add_task/", add_task, name='add_task'),
]
