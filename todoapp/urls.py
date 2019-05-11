from django.urls import path

from main.views import base, users, statistic

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

    # statistic
    path('statistic/', statistic.statistic, name='statistic'),

]
