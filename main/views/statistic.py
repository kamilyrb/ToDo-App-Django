from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from main.models import Todo


@login_required
def statistic(request):
    try:
        cmp_td_count = len(Todo.objects.filter(is_completed=True))
        not_cmp_td_count = len(Todo.objects.filter(is_completed=False))



        return render(request, 'pages/statistic.html', {
            'cmp_count': cmp_td_count,
            'not_cmp_count': not_cmp_td_count,
        })

    except Exception as ex:
        print(ex)
