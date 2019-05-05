# -*- coding: utf-8 -*-
from enum import IntEnum, auto
from operator import itemgetter

from django.utils.translation import ugettext_lazy as _


class BaseEnum(IntEnum):
    @classmethod
    def choices(cls):
        return sorted([(x.value, str(_(x.name))) for x in cls], key=itemgetter(1))

    @classmethod
    def choices_sort_by_key(cls):
        return sorted([(x.value, str(_(x.name))) for x in cls], key=itemgetter(0))

    @classmethod
    def choices_raw(cls):
        return sorted([(x.value, x.name) for x in cls], key=itemgetter(1))


class BuildingType(BaseEnum):
    AVM = 1
    Hospital = 2
    Otel = 3

    @staticmethod
    def translations():
        return [
            _('AVM'),
            _('Hospital'),
            _('Otel'),
        ]


