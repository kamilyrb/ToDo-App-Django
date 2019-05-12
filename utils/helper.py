import datetime
import re
from typing import Any, Union

from django.utils import formats

from main.models import USession
from todoapp.settings import SHORT_DATE_FORMAT, DATE_TIME_FORMAT


class Helper:
    def __init__(self, name='Helper'):
        self.name = name

    @staticmethod
    def format_date_to_str(dtime: datetime, date_format: str = DATE_TIME_FORMAT):
        try:
            return dtime.strftime(date_format)
        except Exception as ex:
            print(ex)

    @staticmethod
    def format_date(source: Any, date_format: str = SHORT_DATE_FORMAT) -> Union[
        str, datetime.datetime]:
        '''
        format datetime object to desired format
        :param source: datetime source
        :param date_format: desired format
        :return:
        '''
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
        '''
        get abstract class object usession.When user login, usession object sets and stores on request.
        :param request:
        :return: USession object from request
        '''
        return USession(**dict(request.session.get('my', {})))

    @staticmethod
    def is_admin(request) -> bool:
        '''
        check user is super_user.It is checking from usession object
        :param request:
        :return:
        '''
        session = Helper.get_session(request)
        return session.is_superuser

    @staticmethod
    def message(text: str = 'Process not done!', success: bool = False, extra_data: dict = ()) -> dict:
        '''
        return dict for use at generally JsonResponse
        :param text:
        :param success:
        :param extra_data:
        :return:
        '''
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
    def get_model_errors(form) -> list:
        '''
        find posted form error and return as list
        :param form:
        :return:
        '''
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
                'message': 'An unknown error occured!',
                'description': ''
            })
        return result

    @staticmethod
    def get_now() -> datetime:
        '''
        get current datetime
        :return:
        '''
        return datetime.datetime.now()

    @staticmethod
    def validate_file_extension(value, extension):
        '''
        Check file extension is equals to param extension
        :param value: file from request
        :param extension: file extension for compare
        :return:
        '''
        import os
        from django.core.exceptions import ValidationError
        ext = os.path.splitext(value.name)[1]
        valid_extensions = [extension]
        if not ext.lower() in valid_extensions:
            raise ValidationError(u'Unsupported file extension.')

    @staticmethod
    def column_index(cname, cols) -> int:
        '''
        Find column index from column headers list
        :param cname: column name
        :param cols: column header list
        :return: int
        '''
        index = 0
        for col in cols:
            if col == cname:
                return index
            index += 1
        return -1
