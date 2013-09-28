
def store_redirect(request, user=None, *args, **kwargs):
    next = request.GET.get('next')
    if user and user.is_authenticated():
        request.session['next'] = next or user.get_absolute_url()
