import json

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import HttpResponse


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class EnsureCSRFMixin(object):

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(EnsureCSRFMixin, self).dispatch(request, *args, **kwargs)


class JSONResponseMixin(object):

    def json_response(self, response):
        return HttpResponse(json.dumps(response), content_type='application/json')

    def get(self, request, *args, **kwargs):
        return self.json_response(self.json_get(request, *args, **kwargs))

    def post(self, request, *args, **kwargs):
        return self.json_response(self.json_post(request, *args, **kwargs))
