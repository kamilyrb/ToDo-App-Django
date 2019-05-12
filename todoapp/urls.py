from django.urls import path

from main.views import base, users, statistic, to_do

urlpatterns = [
    # base
    path('', base.dashboard, name='dashboard'),
    path('login/', base.login, name='login'),
    path('logout/', base.logout, name='logout'),
    path('profile/', base.profile, name='profile'),

    # to_do
    path('todo/form/', to_do.todo_form, name='todo_form'),
    path('todo/form/<int:id>/', to_do.todo_form, name='todo_form'),
    path('todo/export/', to_do.export_todo_list, name='export_todo_list'),
    path('todo/import/', to_do.import_todo_list, name='import_todo_list'),
    path('todo/complete/<int:id>/', to_do.complete_todo, name='complete_todo'),
    path('todo/delete/<int:id>/', to_do.delete_todo, name='delete_todo'),

    # user
    path('user/list/', users.user_list, name='user_list'),
    path('user/form/', users.user_form, name='user_form'),
    path('user/form/<int:id>/', users.user_form, name='user_form'),

    # statistic
    path('statistic/', statistic.statistic, name='statistic'),

]
