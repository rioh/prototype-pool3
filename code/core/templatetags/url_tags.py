import re
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def replace_spaces(value):
    return value.replace(' ', '+')

@register.filter
def replace_underscores(value):
    return value.replace('_', ' ')

@register.filter
def replace_plus_signs(value):
    return value.replace('+', ' ')

@register.filter
def is_list(value):
    return not isinstance(value, str) and hasattr(value, "__iter__")

@register.filter
def format_yes(value):
    """
    Filter to change the format of strings with Yes results to include bold/red styling
    """
    result = re.sub(r'Yes$', '<span style="color:#FF0000;font-weight:bold;">Yes</span>', value)
    return mark_safe(result)
