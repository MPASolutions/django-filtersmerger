import importlib
from django.conf import settings

from django_filtersmerger import RequestFilter


class TotalFilter(RequestFilter):
    """
    TotalFilter joins conditions from all RequestFilter subclasses specified in settings
    """

    def filter_queryset(self, queryset, **kwargs):
        for class_path in settings.FILTER_MERGER_CLASSES:
            module_path, class_name = class_path.rsplit('.', 1)
            module = importlib.import_module(module_path)
            filter_class = getattr(module, class_name)
            # self.filters.append(filter_class(request))
            filter_instance = filter_class()
            filter_instance.set_params(self.get_params())
            queryset = filter_instance.filter_queryset(queryset, **kwargs)
        return queryset
