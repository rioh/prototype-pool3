from django import template
register = template.Library()

@register.filter
def replace_spaces(value):
    return value.replace(' ', '+')

@register.filter
def replace_underscores(value):
    return value.replace('_', ' ')
