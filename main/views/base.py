from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import redirect, render

from main.forms.form import LoginForm
from main.models import USession, Todo
from django.contrib.auth import authenticate, login as sys_login, logout as sys_logout, user_login_failed

from utils.datatable import DataTable
from utils.helper import Helper


@login_required
def dashboard(request):
    try:
        if request.is_ajax():
            data = DataTable.result_list()
            action_list = []

            actions = DataTable.datatable_actions(action_list)

            start = int(request.GET.get('start', 0))
            length = start + int(request.GET.get('length', 10))
            order = DataTable.datatable_order([
                'text',
                'user__username',
                'is_completed',
                'created_time',
                'last_updated',
            ], (int(request.GET.get('order[0][column]', 2)) - 2), request.GET.get('order[0][dir]', 'desc'))

            items = Todo.objects.all()
            total = items.count()
            items = DataTable.filtering(request, items, [
                {'text': 'icontains'},
                {'user__username': 'icontains'},
            ])

            filtered = items.count()
            items = items.order_by(order)[start:length]

            rows = []
            for item in items:
                rows.append({
                    'id': item.id,
                    'text': item.text,
                    'user__username': item.user.username,
                    'is_completed': 'Completed' if item.is_completed else 'Not Completed',
                    'created_time': str(item.created_time),
                    'last_updated':str(item.last_updated),
                    'actions': actions.replace('/0', '/' + str(item.id)).replace('{id}', str(item.id))
                })
            data = DataTable.result_list(True, start, total, filtered, rows)

            return JsonResponse(data)

        return render(request, 'base/list.html', {
            'table': DataTable.datatable([
                {
                    'id': 'text',
                    'title': 'Todo Text',
                    'filter': '<input type="text" class="form-control form-control-sm form-filter m-input">'
                },
                {
                    'id': 'user__username',
                    'title': 'User',
                    'filter': '<input type="text" class="form-control form-control-sm form-filter m-input">'
                }, {
                    'id': 'is_completed',
                    'title': 'Status',
                    'filter': '<input type="text" class="form-control form-control-sm form-filter m-input">'
                }, {
                    'id': 'created_time',
                    'title': 'Created',
                }, {
                    'id': 'last_updated',
                    'title': 'Updated',
                },
            ], url=''),
            'actions': [],

        })
    except Exception as ex:
        print(ex)
        pass


def login(request):
    form = LoginForm(request.POST or None)
    messages = None
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user and user.is_active:
            if not request.POST.get('remember', None):
                request.session.set_expiry(0)

            sys_login(request, user)
            user_session = USession()
            user_session.id = user.id
            user_session.user_id = user.id
            user_session.email = user.email
            user_session.first_name = user.first_name
            user_session.last_name = user.last_name
            user_session.is_superuser = user.is_superuser
            user_session.full_name = user.get_full_name()
            request.session['my'] = model_to_dict(user_session)
            return redirect('dashboard')
        else:
            messages = ['Kullanıcı adı veya parola hatalı']

    return render(request, "pages/login.html", {"form": form, 'messages': messages})


@login_required
def logout(request):
    try:
        sys_logout(request)
        request.session.flush()
        return redirect('/')
    except Exception as ex:
        print(ex)
