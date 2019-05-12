import csv

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404

from main.forms.form import TodoForm
from main.models import Todo
from utils.helper import Helper


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
def complete_todo(request, id):
    result = Helper.message()
    try:
        todo = get_object_or_404(Todo, pk=id)
        if todo.user_id == Helper.get_session(request).id:
            todo.is_completed = True
            todo.last_updated = Helper.get_now()
            todo.save()
            result = Helper.message_success(text='Todo was updated as completed')
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
            result = Helper.message_success(text='Todo was deleted')
        else:
            result['message'] = 'Not Allowed.'
    except Exception as ex:
        result['message'] = str(ex)
    return JsonResponse(result)
