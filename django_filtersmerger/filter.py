class RequestFilter:
    """
    RequestFilter subclasses filter queryset using parameters which can be acquired calling get_param(name).
    We avoid direct access to request to be able to use filters in scripts.

    Filter subclasses may be specified in settings FILTER_MERGER_CLASSES.

    :Example:

    .. code-block:: py

        FILTER_MERGER_CLASSES = [
            'qxs.filters.layer.LayerFilter',  # filters by ModelQxs.filter_queryset()
            'qxs.filters.legacy.LegacyFilter',  # legacy webgis filters
        ]


    .. list-table:: Known implementations (please keep updated if you write a new filter)
       :widths: 25 25 50
       :header-rows: 1

       * - Class
         - Params
         - Description
       * - qxs.filters.layer.LayerFilter
         - LAYER, layer, LAYERS
         - Filters by ModelQxs/RasterQxs.filter_queryset()
       * - qxs.filters.legacy.LegacyFilter
         - LAYER, layer, LAYERS, MPACLASSES, MPAFILTER, filter
         - Filters by ModelQxs/RasterQxs.filters and ModelQxs.classes using params sent by legacy webgis

    """

    def filter_queryset(self, queryset, **kwargs):
        """
        Filter queryset using params. This method must be implemented in subclasses

        :Example:

        .. code-block:: py

            def filter_queryset(self, queryset, **kwargs):
                my_param = self.get_param('MYPARAM')
                if my_param:
                    queryset = queryset.filter(my_param=my_param)
                return queryset

        :param queryset:
        :param kwargs:
        :return:
        """
        return queryset

    def get_param(self, name):
        """
        Get parameter value by name. See RequestFilterParams for details.

        :param name:
        :return: Param value or None if undefined.
        """
        if self._params is None:
            raise Exception("Params not set")
        return self._params.get_param(name)

    # -------------------------------- internals ---------------------------------

    def __init__(self):
        # Params proxy
        self._params = None

    def set_params(self, params):
        self._params = params

    def get_params(self):
        return self._params

    # Note that more filters may share the same param
    # def get_params(self):
    #     """
    #     Get list of request parameter names consumed by this filter. Used to check conflicts of param names.
    #     :return:
    #     """
    #     return []
