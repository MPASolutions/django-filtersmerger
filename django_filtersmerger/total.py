import importlib

from django.conf import settings

from django_filtersmerger import RequestFilter


class TotalFilter(RequestFilter):
    """
    TotalFilter joins conditions from all RequestFilter subclasses specified in settings
    """

    last_applied = None

    def filter_queryset(self, queryset, **kwargs):
        self.last_applied = []
        for class_path in settings.FILTER_MERGER_CLASSES:
            module_path, class_name = class_path.rsplit(".", 1)
            module = importlib.import_module(module_path)
            filter_class = getattr(module, class_name)
            # self.filters.append(filter_class(request))
            filter_instance = filter_class()
            filter_instance.set_params(self.get_params())
            filtered_queryset = filter_instance.filter_queryset(queryset, **kwargs)
            if filtered_queryset != queryset:  # QuerySet does not implement __eq__, objects equality is compared
                self.last_applied.append(class_path)
            queryset = filtered_queryset
        return queryset

    def get_last_applied(self):
        return self.last_applied
