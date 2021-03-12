from django_filtersmerger.params import RequestFilterParams, DictFilterParams
from django_filtersmerger.total import TotalFilter


class FilterMerger:
    """
    This class puts together all classes defined in FILTER_MERGER_CLASSES settings.

    :Example:

    .. code-block:: py

        from django_filtersmerger import FilterMerger
        filter_merger = FilterMerger(request=self.request)
        queryset = filter_merger.get_queryset(model)

    """

    def __init__(self, request=None, params=None):
        """
        :param request:
        :param params: dictionary with params
        """
        self.request = request
        self.params = params
        # list of last classes which changed queryset
        self.last_applied = None

    def get_queryset(self, model, initial_queryset=None):
        """
        Get queryset filtered by all registered filters
        :param model:
        :return:
        """
        if initial_queryset is not None:
            queryset = initial_queryset
        else:
            queryset = model.objects.all()
        queryset = self.filter_queryset(queryset)
        return queryset

    def get_queryset_applied(self, model):
        """
        Get queryset filtered by all registered filters and list of applied RequestFilter classes
        :param model:
        :return:
        """
        queryset = model.objects.all()
        queryset, applied = self.filter_queryset_applied(queryset)
        return queryset, applied

    def filter_queryset(self, queryset):
        """
        Filter queryset by all registered filters
        :param queryset:
        :return:
        """
        queryset, applied = self.filter_queryset_applied(queryset)
        return queryset

    def filter_queryset_applied(self, queryset):
        """
        Filter queryset by all registered filters and get list of applied RequestFilter classes
        :param queryset:
        :return:
        """
        if self.request:
            params_proxy = RequestFilterParams(self.request)
        elif self.params:
            params_proxy = DictFilterParams(self.params)

        total_filter = TotalFilter()
        total_filter.set_params(params_proxy)

        queryset = total_filter.filter_queryset(queryset)

        self.last_applied = total_filter.get_last_applied()

        return queryset, self.last_applied

    def get_last_applied(self):
        return self.last_applied

    def get_last_debug_headers(self):
        headers = {
            'MpaFilterApplied': ','.join(self.last_applied) if self.last_applied else ''
        }
        return headers
