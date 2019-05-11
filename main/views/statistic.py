from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render

from main.models import Todo

@login_required
def statistic(request):
    try:
        cmp_td_count = len(Todo.objects.filter(is_completed=True))
        not_cmp_td_count = len(Todo.objects.filter(is_completed=False))
        users = []
        user_todo_counts = []
        for u in User.objects.all():
            users.append(u.username)
            user_todo_counts.append(len(Todo.objects.filter(user_id=u.id)))
        user_todo_counts.append(0)

        return render(request, 'pages/statistic.html', {
            'cmp_count': cmp_td_count,
            'not_cmp_count': not_cmp_td_count,
            'users': users,
            'user_todo_counts': user_todo_counts
        })

    except Exception as ex:
        print(ex)
