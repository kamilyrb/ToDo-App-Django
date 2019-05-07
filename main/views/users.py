from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

from utils.datatable import DataTable


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
                },
            ], url=''),
            'actions': [{
                'label': 'Yeni Kayıt',
                'class': 'btn btn-primary',
                'icon': 'icon-plus',
            }],

        })
    except Exception as ex:
        print(ex)
        pass