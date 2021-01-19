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
    extra_filter_params = {}
    spatial_filter_params = {}
    for class_path in settings.FILTER_MERGER_CLASSES:
        module_path, class_name = class_path.rsplit('.', 1)
        module = importlib.import_module(module_path)
        filter_class = getattr(module, class_name)
        filter_params[class_name] = getattr(filter_class, 'PARAM', None)
        if class_name not in ['DjangoAdvancedOTFWebixFilter', 'DjangoAdvancedWebixFilter', 'SpatialFilter', 'DjangoBaseWebixFilter']:
            extra_filter_params[class_name] = getattr(filter_class, 'PARAM', None)
        if class_name in ['SpatialFilter']:
            spatial_filter_params[class_name] = getattr(filter_class, 'PARAM', None)
    # filter_params lista di tutti i filter param inizializzati nei settings
    # extra_filter_params lista dei filtri da disattivare nel bottton "extra filter remove" sulla lista
    # spatial_filter_params lista dei filtri da disattivare nel bottone "Geo filter remove" sulla lista
    context['filter_params'] = filter_params
    context['extra_filter_params'] = extra_filter_params
    context['spatial_filter_params'] = spatial_filter_params
    return ''
