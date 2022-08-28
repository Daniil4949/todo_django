from django.urls import path, include
from .views import RegisterUser, MainPage, add_task, profile, mark_as_comleted, delete_task, delete_all_tasks, LoginUser, logout_user

urlpatterns = [
    path('main/', MainPage.as_view(), name='home'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path("add_task/", add_task, name='add_task'),
    path("profile/", profile, name='profile'),
    path("mark_as_completed/<slug:slug>/", mark_as_comleted, name='mark_as_completed'),
    path("delete_task/<slug:slug>/", delete_task, name='delete_task'),
    path("delete_all_tasks/", delete_all_tasks, name='delete_all_tasks'),
]
