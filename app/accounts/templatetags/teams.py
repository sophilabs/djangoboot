from django import template


register = template.Library()


@register.filter
def has_user(team, user):
    if user.is_authenticated():
        return team.has_user(user)
    else:
        return False
