from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import get_password_validators
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from main.forms.form import UserForm
from todoapp.settings import AUTH_PASSWORD_VALIDATORS
from utils.datatable import DataTable
from utils.helper import Helper


@login_required
def user_list(request):
    try:
        if request.is_ajax():
            data = DataTable.result_list()
            action_list = []

            actions = DataTable.datatable_actions(action_list)

            start = int(request.GET.get('start', 0))
            length = start + int(request.GET.get('length', 10))
            order = DataTable.datatable_order([
                'first_name',
                'last_name',
                'last_login',
            ], (int(request.GET.get('order[0][column]', 2)) - 2), request.GET.get('order[0][dir]', 'desc'))

            items = User.objects.all()
            total = items.count()
            items = DataTable.filtering(request, items, [
                {'first_name': 'icontains'},
                {'last_name': 'icontains'},
            ])

            filtered = items.count()
            items = items.order_by(order)[start:length]

            rows = []
            for item in items:
                rows.append({
                    'id': item.id,
                    'first_name': item.first_name,
                    'last_name': item.last_name,
                    'last_login':Helper.format_date_to_str(item.last_login) if item.last_login else '',
                    'actions': actions.replace('/0', '/' + str(item.id)).replace('{id}', str(item.id))
                })
            data = DataTable.result_list(True, start, total, filtered, rows)

            return JsonResponse(data)

        return render(request, 'base/list.html', {
            'table': DataTable.datatable([
                {
                    'id': 'first_name',
                    'title': 'First Name',
                    'filter': '<input type="text" class="form-control form-control-sm form-filter m-input">'
                },
                {
                    'id': 'last_name',
                    'title': 'Last Name',
                    'filter': '<input type="text" class="form-control form-control-sm form-filter m-input">'
                }, {
                    'id': 'last_login',
                    'title': 'Last Login',
                },
            ], url=''),
            'actions': [{
                'label': 'New Record',
                'class': 'btn btn-primary',
                'icon': 'icon-plus',
                'onclick': "App.dialogForm('New User', '" + reverse('user_form', args=[0]) + "',{'large':true})"
            }],

        })
    except Exception as ex:
        print(ex)
        pass


@login_required
def user_form(request, id=None):
    try:
        item = User.objects.get(pk=id) if id else User()
        if request.is_ajax() and request.method == 'POST':
            result = Helper.message_success()

            form = UserForm(request.POST or None, instance=item)

            if form.is_valid():
                m: User = form.save(commit=False)
                pass_change = False

                if 'password' in form.data and len(form.data['password']) > 0:
                    errors = []
                    for validator in get_password_validators(AUTH_PASSWORD_VALIDATORS):
                        try:
                            validator.validate(form.data['password'], None)
                        except ValidationError as error:
                            errors.append(error)

                    # check for digit
                    if not any(char.isdigit() for char in form.data['password']):
                        errors.append(ValidationError('Şifre en az bir tane rakam içermelidir'))

                    # check for letter
                    if not any(char.isalpha() for char in form.data['password']):
                        errors.append(ValidationError('Şifre en az bir tane harf içermelidir'))

                    if errors:
                        result['message'] = '<br>'.join([x.messages[0] for x in errors])
                        return JsonResponse(result)
                    else:
                        pass_change = True
                if id:
                    users = User.objects.filter(username=form.cleaned_data['username']).exclude(id=id)
                    if len(users) > 0:
                        result['message'] = 'Bu kullanıcı adına ait bir kayıt zaten mevcut!'
                        return JsonResponse(result)

                    users = User.objects.filter(email=form.cleaned_data['email']).exclude(id=id)
                    if len(users) > 0:
                        result['message'] = 'Bu mail adresine ait bir kayıt zaten mevcut!'
                        return JsonResponse(result)

                else:
                    users = User.objects.filter(username=form.cleaned_data['username']).exclude(id=id)
                    if len(users) > 0:
                        result['message'] = 'Bu kullanıcı adına ait bir kayıt zaten mevcut!'
                        return JsonResponse(result)

                    users = User.objects.filter(email=form.cleaned_data['email']).exclude(id=id)
                    if len(users) > 0:
                        result['message'] = 'Bu mail adresine ait bir kayıt zaten mevcut!'
                        return JsonResponse(result)
                if pass_change:
                    m.set_password(form.data['password'])
                m.save()
                result = Helper.message_success()
            else:
                error = Helper.get_model_errors(form)
                result['message'] = error[0]['label'] + ': ' + error[0]['message']
            return JsonResponse(result)

        context = {
            'form': item,
        }
        return render(request, 'pages/user/form.html', context)
    except Exception as ex:
        print(ex)