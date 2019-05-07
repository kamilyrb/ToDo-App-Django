import datetime
from typing import Any

from main.models import USession


class Helper:
    def __init__(self, name='Helper'):
        self.name = name

    @staticmethod
    def format_date_to_str(dtime:datetime,date_format:str):
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