from filtermerger.params import RequestFilterParams, DictFilterParams
from filtermerger.total import TotalFilter


class FilterMerger:
    """
    This class puts together all classes defined in FILTER_MERGER_CLASSES settings.

    :Example:

    .. code-block:: py

        from filtermerger import FilterMerger
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

    def get_queryset(self, model):
        """
        Get queryset filtered by all registered filters
        :param model:
        :return:
        """
        queryset = model.objects.all()
        queryset = self.filter_queryset(queryset)
        return queryset

    def filter_queryset(self, queryset):
        if self.request:
            params_proxy = RequestFilterParams(self.request)
        elif self.params:
            params_proxy = DictFilterParams(self.params)

        total_filter = TotalFilter()
        total_filter.set_params(params_proxy)

        queryset = total_filter.filter_queryset(queryset)

        return queryset
