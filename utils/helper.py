import datetime
from typing import Any

from main.models import USession


class Helper:
    def __init__(self, name='Helper'):
        self.name = name

    @staticmethod
    def format_date_to_str(dtime: datetime, date_format: str):
        try:
            return dtime.strftime(date_format)
        except Exception as ex:
            print(ex)

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
    def message_success(text: str = 'Kaydedildi...', extra_data: dict = ()) -> dict:
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

