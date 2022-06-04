from django.http import HttpResponseRedirect
from django.urls import resolve


class CustomeMiddlware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if request.user.is_authenticated:
            response = self.get_response(request)
            return response

        else:
            if resolve(request.path_info).url_name != 'login_url':
                return HttpResponseRedirect('/login/')
            return  self.get_response(request)
            

        # Code to be executed for each request/response after
        # the view is called.
