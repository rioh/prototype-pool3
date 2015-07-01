from django import template
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
    return hasattr(value, "__iter__")

