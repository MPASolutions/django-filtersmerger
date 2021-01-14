# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import template
from django.conf import settings
import importlib

register = template.Library()


@register.filter('request_filter_param')
def request_filter_param(class_name_searched):
    for class_path in settings.FILTER_MERGER_CLASSES:
        module_path, class_name = class_path.rsplit('.', 1)
        module = importlib.import_module(module_path)
        filter_class = getattr(module, class_name)
        if class_name_searched == class_name:
            return getattr(filter_class, 'PARAM', None)
    return None


@register.simple_tag(takes_context=True)
def get_request_filter_params(context):
    filter_params = {}
    for class_path in settings.FILTER_MERGER_CLASSES:
        module_path, class_name = class_path.rsplit('.', 1)
        module = importlib.import_module(module_path)
        filter_class = getattr(module, class_name)
        filter_params[class_name] = getattr(filter_class, 'PARAM', None)
    context['filter_params'] = filter_params
    return ''
