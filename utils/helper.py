import csv
import datetime
import re
from typing import Any, Union

from django.http import HttpResponse
from django.utils import formats

from main.models import USession
from todoapp.settings import SHORT_DATE_FORMAT, DATE_TIME_FORMAT


class Helper:
    def __init__(self, name='Helper'):
        self.name = name

    @staticmethod
    def format_date_to_str(dtime: datetime, date_format :str = DATE_TIME_FORMAT):
        try:
            return dtime.strftime(date_format)
        except Exception as ex:
            print(ex)

    @staticmethod
    def format_date(source: Any, date_format: str = SHORT_DATE_FORMAT) -> Union[
        str, datetime.datetime]:
        formatted = None
        if isinstance(source, str):
            splitted = re.split(r'[/\-.\s]+', source)
            if len(splitted) > 2:
                year = splitted[0]
                month = splitted[1]
                day = splitted[2]

                if len(splitted[0]) == 2:
                    year = splitted[2]
                    day = splitted[0]

                formatted = datetime.datetime(year=int(year), month=int(month), day=int(day))
        elif isinstance(source, (datetime.date, datetime.datetime)):
            formatted = source

        return formats.date_format(formatted, date_format) if formatted else ''

    @staticmethod
    def get_session(request) -> USession:
        return USession(**dict(request.session.get('my', {})))

    @staticmethod
    def is_admin(request) -> bool:
        session = Helper.get_session(request)
        return session.is_superuser

    @staticmethod
    def message(text: str = 'İşlem yapılmadı!', success: bool = False, extra_data: dict = ()) -> dict:
        result = {
            'success': success,
            'message': text
        }

        if extra_data:
            for key, value in iter(extra_data.items()):
                result[key] = value

        return result

    @staticmethod
    def message_success(text: str = 'Saved...', extra_data: dict = ()) -> dict:
        return Helper.message(text, True, extra_data)

    @staticmethod
    def get_model_errors(form):
        result = []

        for key in form.errors.keys():
            try:
                label = ''
                description = ''

                try:
                    label = form.instance._meta.get_field(key).verbose_name
                    description = form.instance._meta.get_field(key).help_text
                except Exception:
                    try:
                        label = key
                        description = form.fields[key].help_text
                    except Exception:
                        pass
                    pass

                result.append({
                    'field_list': key,
                    'label': label,
                    'message': form.errors[key][0],
                    'description': description
                })
            except Exception:
                pass
        if len(result) == 0:
            result.append({
                'field_list': '',
                'label': '',
                'message': 'Nedeni belirlenemeyen bir hata oluştu!',
                'description': ''
            })
        return result


    @staticmethod
    def get_now():
        return datetime.datetime.now()

    @staticmethod
    def export_to_excel(rows: list, file_name: str = 'Liste') -> HttpResponse:
        response = HttpResponse(content_type='text/csv')
        response.write('\ufeff')

        data = csv.writer(response, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)

        for row in rows:
            data.writerow(row)

        response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
        response['Content-Type'] = 'text/csv'
        return response


