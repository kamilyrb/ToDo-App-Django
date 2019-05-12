from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from main.forms.form import LoginForm
from main.models import USession, Todo
from django.contrib.auth import authenticate, login as sys_login, logout as sys_logout

from utils.datatable import DataTable
from utils.helper import Helper


@login_required
def dashboard(request):
    try:
        if request.is_ajax():
            data = DataTable.result_list()
            delete_action_list = [{
                'title': 'Delete',
                'icon': 'fa fa-times color-danger',
                'message': 'Do you want to delete this todo?',
                'event': 'confirm',
                'confirmurl': reverse('delete_todo', args=[0]),
            }]
            comp_and_del_action_list = [{
                'title': 'Complete Todo',
                'icon': 'fa fa-check color-success',
                'message': 'Do you want to complete this todo?',
                'event': 'confirm',
                'confirmurl': reverse('complete_todo', args=[0]),
            }, {
                'title': 'Delete',
                'icon': 'fa fa-times color-danger',
                'message': 'Do you want to delete this todo?',
                'event': 'confirm',
                'confirmurl': reverse('delete_todo', args=[0]),
            }]
            delete_action = DataTable.datatable_actions(delete_action_list)
            comp_and_del_action = DataTable.datatable_actions(comp_and_del_action_list)

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
                'is_completed'
            ])

            filtered = items.count()
            items = items.order_by(order)[start:length]

            rows = []
            for item in items:
                actions = delete_action if item.is_completed else comp_and_del_action
                rows.append({
                    'id': item.id,
                    'text': item.text,
                    'user__username': item.user.username,
                    'is_completed': 'Completed' if item.is_completed else 'Not Completed',
                    'created_time': Helper.format_date_to_str(item.created_time),
                    'last_updated': Helper.format_date_to_str(item.last_updated),
                    'actions': actions.replace('/0', '/' + str(item.id))
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
                    'filter': '<select class="form-control form-control-sm form-filter m-input">' + DataTable.datatable_filter_options(
                        [('true', 'Completed'), ('false', 'Not Completed')]) + '</select>'
                }, {
                    'id': 'created_time',
                    'title': 'Created',
                }, {
                    'id': 'last_updated',
                    'title': 'Updated',
                },
            ], url=''),
            'actions': [{
                'label': 'Export',
                'class': 'btn btn-success',
                'icon': 'icon-plus',
                'target': '_blank',
                'url': reverse('export_todo_list')
            }, {
                'label': 'Import',
                'class': 'btn btn-info',
                'icon': 'icon-plus',
                'onclick': "App.dialogForm('Import Todo', '" + reverse('import_todo_list') + "')"
            }, {
                'label': 'New Record',
                'class': 'btn btn-primary',
                'icon': 'icon-plus',
                'onclick': "App.dialogForm('New Todo', '" + reverse('todo_form', args=[0]) + "')"
            }],

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
            messages = ['Invalid password or username.']

    return render(request, "pages/login.html", {"form": form, 'messages': messages})


@login_required
def logout(request):
    try:
        sys_logout(request)
        request.session.flush()
        return redirect('/')
    except Exception as ex:
        print(ex)


@login_required
def profile(request):
    try:
        return render(request, 'pages/profile.html', {'form': User.objects.get(pk=Helper.get_session(request).user_id)})
    except Exception as ex:
        print(ex)
