from django.shortcuts import redirect


def perform_redirect(request, user=None, *args, **kwargs):
    next = request.GET.get('next')
    if user and user.is_authenticated():
        return redirect(next or user.get_absolute_url())
