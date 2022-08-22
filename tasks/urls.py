from django.urls import path, include
from .views import RegisterUser, MainPage, add_task, profile, mark_as_comleted, delete_task, delete_all_tasks

urlpatterns = [
    path('main/', MainPage.as_view(), name='home'),
    path('accounts/registration/', RegisterUser.as_view(), name='registration'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("add_task/", add_task, name='add_task'),
    path("profile/", profile, name='profile'),
    path("mark_as_completed/<slug:slug>/", mark_as_comleted, name='mark_as_completed'),
    path("delete_task/<slug:slug>/", delete_task, name='delete_task'),
    path("delete_all_tasks/", delete_all_tasks, name='delete_all_tasks'),

]
