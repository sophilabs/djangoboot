from django.conf import settings as dsettings


def settings(request):
    return {
        'STATIC_DOMAIN': dsettings.STATIC_DOMAIN
    }