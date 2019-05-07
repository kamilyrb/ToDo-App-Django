# -*- coding: utf-8 -*-
from django.urls import reverse

# from utils.enums
# from utils.helper
from utils.helper import Helper

page_title = None
breadcrumbs = []

notifications = {
    'updates': None,
    'online': []
}


def defaults(request):
    return {
        'is_admin': Helper.is_admin(request),
    }


def set_page_title(title):
    global page_title
    page_title = title
