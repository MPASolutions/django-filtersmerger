import json


class FilterParams:
    """
    Filter parameters base class.
    """

    def get_param(self, name):
        """
        Get parameter value by name. This method must be implemented in subclasses.
        :param name:
        :return: Param value or None if undefined.
        """
        return None


class RequestFilterParams:
    """
    Gets filter parameters from request in this order:
      * GET <name> param: URL param /path/?MYFILTER=123
      * POST <name> param: posted form data MYFILTER: 123
      * <name> property from 'post' GET param loaded as JSON: /path/?post={"MYFILTER": 123}, currently not used by web clients, useful for debugging
      * <name> property from request body JSON: request payload: {"MYFILTER": 123}
    """

    def __init__(self, request):
        self.request = request
        self.data = None

        data_str = self.request.GET.get('post')

        # legacy webgis is sending 'filter' param in json body or as param
        if not data_str and self.request.body and self.request.is_ajax():
            data_str = self.request.body.decode()

        if data_str:
            self.data = json.loads(data_str)

    def get_param(self, name):
        if name in self.request.GET:
            return self.request.GET.get(name)

        if name in self.request.POST:
            return self.request.POST.get(name)

        if self.data:
            return self.data.get(name)

        return None


class DictFilterParams:
    """
    Gets filter parameters from dictionary.
    """

    def __init__(self, params):
        self.params = params

    def get_param(self, name):
        return self.params.get(name)
