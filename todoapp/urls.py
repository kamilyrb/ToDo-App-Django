"""todoapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path

from main.views import base, users

urlpatterns = [
    # base
    path('', base.dashboard, name='dashboard'),
    path('login/', base.login, name='login'),
    path('logout/', base.logout, name='logout'),
    path('todo/form/', base.todo_form, name='todo_form'),
    path('todo/form/<int:id>/', base.todo_form, name='todo_form'),
    path('todo/export/', base.export_todo_list, name='export_todo_list'),
    path('todo/import/', base.import_todo_list, name='import_todo_list'),
    path('todo/complete/<int:id>/', base.complete_todo, name='complete_todo'),
    path('todo/delete/<int:id>/', base.delete_todo, name='delete_todo'),

    # user
    path('user/list/', users.user_list, name='user_list'),
    path('user/form/', users.user_form, name='user_form'),
    path('user/form/<int:id>/', users.user_form, name='user_form'),

    # profile
    path('profile/', base.profile, name='profile'),

]
