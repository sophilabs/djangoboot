from django import template

from boots.models import Star

register = template.Library()


@register.simple_tag(takes_context=True)
def star_button(context, boot, css_class=''):
    user = context.get('user')

    if user.is_authenticated() and Star.objects.filter(user=user, boot=boot):
        value = 'true'
        icon_class = 'icon-heart'
    else:
        value = 'false'
        icon_class = 'icon-heart-empty'

    return '<a class="btn btn-primary btn-sm btn-star-boot %s" data-boot-id="%s" data-value="%s" href="#">' \
           '<i class="%s"></i> <span class="count">%s</span></a>' % (css_class, boot.id, value, icon_class,
                                                                     boot.stars.count())
