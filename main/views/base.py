import csv
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse

from main.forms.form import LoginForm, TodoForm
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
def todo_form(request, id=None):
    try:
        item = Todo.objects.get(pk=id) if id else Todo()
        if request.is_ajax() and request.method == 'POST':
            result = Helper.message_success()

            form = TodoForm(request.POST or None, instance=item)

            if form.is_valid():
                m: Todo = form.save(commit=False)
                # m.last_updated = Helper.get_now()
                m.save()
                result = Helper.message_success()
            else:
                error = Helper.get_model_errors(form)
                result['message'] = error[0]['label'] + ': ' + error[0]['message']
            return JsonResponse(result)

        context = {
            'form': item,
            'users': User.objects.all().values('id', 'username')
        }
        return render(request, 'pages/todo/form.html', context)
    except Exception as ex:
        print(ex)


@login_required
def export_todo_list(request):
    try:
        file_name = 'todo_list.csv'
        todos = Todo.objects.all()
        response = HttpResponse(content_type='text/csv')
        response.write('\ufeff')

        data = csv.writer(response, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
        data.writerow(['User', 'Todo', 'Status', 'Created', 'Updated'])
        for t in todos:
            data.writerow([t.user.username, t.text, 'Completed' if t.is_completed else 'Not Completed',
                           Helper.format_date_to_str(t.created_time), Helper.format_date_to_str(t.last_updated)])

        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
        response['Content-Type'] = 'text/csv'
        return response

    except Exception as ex:
        print(ex)


@login_required
def import_todo_list(request):
    if request.method == 'POST':
        result = Helper.message()
        try:
            file = request.FILES.get('csv_file', None)
            try:
                Helper.validate_file_extension(file, '.csv')
            except ValidationError:
                result['message'] = 'File type is not valid.Please select a csv file.'

            decoded_file = file.read().decode('ISO-8859-1').replace('ï»¿', '').splitlines()
            file_content = list(csv.reader(decoded_file, delimiter=';', quotechar='"'))
            header = file_content.pop(0)
            todo_index = Helper.column_index('Todo', header)
            status_index = Helper.column_index('Status', header)
            authenticated_user_id = Helper.get_session(request).user_id
            if todo_index is not -1 and status_index is not -1:
                for r in file_content:
                    try:
                        Todo.objects.create(user_id=authenticated_user_id, text=r[todo_index].strip(),
                                            is_completed=False if 'Not Completed' in r[status_index] else True)
                    except Exception as ex:
                        print(ex)
                result = Helper.message_success(text='Records are created.')
            else:
                result['message'] = 'File format is not valid.'

        except Exception as ex:
            print(ex)
            result['message'] = str(ex)
        return JsonResponse(result)

    return render(request, 'pages/todo/import_form.html', {})


@login_required
def profile(request):
    try:
        return render(request, 'pages/profile.html', {'form': User.objects.get(pk=Helper.get_session(request).user_id)})
    except Exception as ex:
        print(ex)


@login_required
def complete_todo(request, id):
    result = Helper.message()
    try:
        todo = get_object_or_404(Todo, pk=id)
        if todo.user_id == Helper.get_session(request).id:
            todo.is_completed = True
            todo.last_updated = Helper.get_now()
            todo.save()
            result = Helper.message_success(text='Todo is updated as completed')
        else:
            result['message'] = 'Not Allowed.'
    except Exception as ex:
        result['message'] = str(ex)
    return JsonResponse(result)


@login_required
def delete_todo(request, id):
    result = Helper.message()
    try:
        todo = get_object_or_404(Todo, pk=id)
        if todo.user_id == Helper.get_session(request).id:
            todo.delete()
            result = Helper.message_success(text='Todo is deleted')
        else:
            result['message'] = 'Not Allowed.'
    except Exception as ex:
        result['message'] = str(ex)
    return JsonResponse(result)