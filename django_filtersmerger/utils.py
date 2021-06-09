import importlib
from django.conf import settings


def get_request_filter(class_path):
    module_path, class_name = class_path.rsplit('.', 1)
    module = importlib.import_module(module_path)
    filter_class = getattr(module, class_name)
    return filter_class


def get_registered_filters_param(filter_name=None):

    if filter_name is not None:

        for class_path in settings.FILTER_MERGER_CLASSES:
            request_filter = get_request_filter(class_path)

            if filter_name == request_filter.__name__:
                return getattr(request_filter, 'PARAM', None)

        return None

    elif filter_name is None:

        filter_params = {}
        extra_filter_params = {}
        spatial_filter_params = {}

        for class_path in settings.FILTER_MERGER_CLASSES:
            request_filter = get_request_filter(class_path)
            class_name = request_filter.__name__
            filter_param = getattr(request_filter, 'PARAM', None)

            # filter_params: lista di tutti i filter param registarti nei settings
            filter_params[class_name] = filter_param

            # extra_filter_params: lista dei filtri da disattivare nel bottton "extra filter remove" sulla lista
            if class_name not in [  # keep all registered filter except:
                'DjangoBaseWebixFilter',  # base list column filter (manaul cleaning)
                'DjangoAdvancedOTFWebixFilter', 'DjangoAdvancedWebixFilter',  # advanced filter mnaged in specific popup
                'SpatialFilter'  # satial filter disabled by specifc button (defined below)
            ]:
                extra_filter_params[class_name] = filter_param

            # spatial_filter_params: lista dei filtri da disattivare nel bottone "Geo filter remove" sulla lista
            if class_name in ['SpatialFilter']:
                spatial_filter_params[class_name] = filter_param

        return {
            'registered_filters': filter_params,
            'extra_filter': extra_filter_params,
            'spatial_filter': spatial_filter_params,
        }

