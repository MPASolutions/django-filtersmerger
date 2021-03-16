# -*- coding: utf-8 -*-

from django import template
from django_filtersmerger.utils import get_regsitered_filters_param

register = template.Library()


@register.filter('request_filter_param')
def request_filter_param(filter_name):
    """
    get specific filter PARAM for given filter class
    :param filter_name: filter name (class) of the requested param
    :return:
    """
    return get_regsitered_filters_param(filter_name)


@register.simple_tag(takes_context=True)
def get_request_filter_params(context):
    """
    get full dicts with {class: PARAM} foreach FILTER_MERGER_CLASSES, and specific dicts for extra and spatial filter
    :param context:
    :return:
    """
    filter_params = get_regsitered_filters_param()

    context['filter_params'] = filter_params['regsitered_filters']
    context['extra_filter_params'] = filter_params['extra_filter']
    context['spatial_filter_params'] = filter_params['spatial_filter']
    return ''
