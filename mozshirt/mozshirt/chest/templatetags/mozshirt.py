import hashlib
from django import template

register = template.Library()

@register.filter
def gravatar(user, size=48):
    return ('https://gravatar.com/avatar/%s?s=%s' %
            (hashlib.md5(user.email).hexdigest(), size))
