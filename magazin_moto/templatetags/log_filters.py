# magazin_moto/templatetags/log_filters.py
from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(obj, key):

    if hasattr(obj, key):
        return getattr(obj, key)
    elif isinstance(obj, dict):
        return obj.get(key)
    return None