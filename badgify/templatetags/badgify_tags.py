# -*- coding: utf-8 -*-
from django import template

from ..models import Badge, Award
from ..compat import get_user_model


register = template.Library()
register_tag = register.assignment_tag if hasattr(register, 'assignment_tag') else register.simple_tag


@register_tag
def badgify_badges(**kwargs):
    """
    Returns all badges or only awarded badges for the given user.
    """
    User = get_user_model()
    user = kwargs.get('user', None)
    username = kwargs.get('username', None)
    if username:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            pass
    if user:
        awards = Award.objects.filter(user=user).select_related('badge')
        badges = [award.badge for award in awards]
        return badges
    return Badge.objects.all()
