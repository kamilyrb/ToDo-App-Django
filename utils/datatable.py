from typing import Union, Any

from django.db.models import QuerySet


class DataTable:
    def __init__(self, name='DataTable'):
        self.name = name

    @staticmethod
    def datatable(columns: list,
                  id: str = None,
                  url: str = None,
                  checkable: bool = False,
                  numbering: bool = True,
                  actions: bool = True,
                  sorting: dict = (),
                  hide: int = 5,
                  export_all:bool = False,
                  classname: str = None,
                  rowcallback: str = None,
                  initcomplete: str = None,
                  drawcallback: str = None,
                  actions_title: str = 'İşlem'
                  ) -> dict:
        """ Datatables architecture
        :param columns: list [{ 'id', 'title', 'class', 'sortable', 'filter' }]
        :param id: str
        :param url: str
        :param checkable: bool
        :param numbering: bool
        :param actions: bool
        :param sorting: dict { 'column', 'dir' }
        :param hide: int
        :param export_all: bool
        :param classname: str
        :param rowcallback: str
        :param drawcallback: str
        :param initcomplete: str
        :param actions_title: str



        :return: str
        """

        # Check table has filtering column
        filters = False

        for column in columns:
            try:
                if column['filter']:
                    filters = True
            except Exception:
                pass

        return {
            'id': id,
            'url': url,
            'checkable': checkable,
            'numbering': numbering,
            'columns': columns,
            'filters': filters,
            'actions': actions,
            'sorting': sorting,
            'hide': hide,
            'export_all': str(export_all).lower(),
            'classname': classname,
            'rowcallback': rowcallback,
            'initcomplete': initcomplete,
            'drawcallback': drawcallback,
            'actions_title': actions_title
        }

    @staticmethod
    def datatable_actions(actions: list) -> str:
        buttons = []

        for action in actions:
            buttons.append(
                '<a href="' + (action['url'] if 'url' in action else 'javascript:;') + '"'
                + ' class="m-portlet__nav-link btn m-btn m-btn--hover-brand m-btn--icon m-btn--icon-only m-btn--pill ' + (action['class'] if 'class' in action else '') + '"'
                + (' title="' + action['title'] + '"' if 'title' in action else '')
                + (' target="' + action['target'] + '"' if 'target' in action else '')
                + (' data-title="' + action['title'] + '"' if 'title' in action else '')
                + (' data-event="' + action['event'] + '"' if 'event' in action else '')
                + (' data-message="' + action['message'] + '"' if 'message' in action else '')
                + (' data-id="' + action['id'] + '"' if 'id' in action else '')
                + (' data-confirmurl="' + action['confirmurl'] + '"' if 'confirmurl' in action else '')
                + (' onclick="' + action['onclick'] + '"' if 'onclick' in action else '') + '>'
                + '<i class="' + (action['icon'] if 'icon' in action else 'fas fa-edit') + '"></i>'
                + (' (' + action['badge'] + ') ' if 'badge' in action else '') + '</a>'
            )

        return "\n".join(buttons)

    @staticmethod
    def datatable_filter_options(options: Union[list, dict, QuerySet], add_empty: bool = True,
                                 value_field: str = 'title', id_field: str = 'id',
                                 selected_value: Union[str, None] = None) -> str:
        result = []
        if add_empty:
            result.append('<option value="">-- Select --</option>')

        try:
            if isinstance(options, list):
                for key, opt in options:
                    if isinstance(opt, dict):
                        result.append('<option value="' + str(opt[0]) + '">' + str(opt[1]) + '</option>')
                    else:
                        result.append('<option value="' + str(key) + '">' + str(opt) + '</option>')
            elif isinstance(options, dict):
                for k, v in options:
                    result.append('<option value="' + str(k) + '">' + str(v) + '</option>')

            elif isinstance(options, QuerySet):
                for opt in options:
                    if isinstance(opt, dict):
                        result.append(
                            '<option value="' + str(opt[id_field]) + '">' + str(opt[value_field]) + '</option>')
                    else:
                        result.append('<option value="' + str(getattr(opt, id_field)) + '">' + str(
                            getattr(opt, value_field)) + '</option>')

            if selected_value:
                for index, row in enumerate(result):
                    if 'value="' + str(selected_value) + '"' in row:
                        result[index] = row.replace('value=', 'selected value=')
                        break
        except Exception:
            pass

        return "\n".join(result)

    @staticmethod
    def filtering(request, items, columns):
        try:
            kwargs = {}
            for element in columns:
                if isinstance(element, dict):
                    column, filter_type = next(iter(element.items()))
                    filter_name = '{0}__{1}'.format(column, filter_type)
                else:
                    column = element
                    filter_name = element
                incoming = request.GET.get(column)
                if incoming and len(incoming):
                    if incoming in ['true', 'false']:
                        incoming = True if incoming == 'true' else False
                    kwargs[filter_name] = incoming
            if len(kwargs):
                items = items.filter(**kwargs)
        except Exception as ex:
            print(ex)
            pass

        return items

    @staticmethod
    def array_value(array: Union[dict, list], key_name: Union[int, str], default: str = None) -> Any:
        item = default

        if isinstance(array, dict) or isinstance(array, list):
            try:
                if isinstance(array, list):
                    key_name = int(key_name)

                item = array[key_name]
            except KeyError:
                pass
            except IndexError:
                pass

        return item

    @staticmethod
    def array_first(array: Union[dict, list], item_type: str = 'value') -> Any:
        item = None
        item_key = None
        item_value = None

        try:
            if isinstance(array, dict):
                item_key, item_value = array.popitem()
            elif isinstance(array, list):
                item_key = 0
                item_value = array.pop(0)
        except KeyError:
            pass
        except IndexError:
            pass

        if item_key or item_value:
            if item_type == 'key':
                item = item_key
            else:
                item = item_value

        return item

    @staticmethod
    def datatable_order(array: Union[dict, list], key_name: Union[int, str], direction: str = 'desc') -> str:
        field = DataTable.array_value(array, key_name)

        if field is None:
            field = DataTable.array_first(array)

        order = '-' if direction == 'desc' else ''

        return order + field

    @staticmethod
    def result_values(success: bool = False, data: Union[list, dict, str] = ()) -> dict:
        return {
            'success': success,
            'data': data
        }

    @staticmethod
    def result_list(success: bool = False, start: int = 0, total: int = 0, filtered_total: int = 0,
                    data: list = ()) -> dict:
        return {
            'success': success,
            'recordsTotal': total,
            'recordsFiltered': filtered_total,
            'start': start,
            'data': data
        }