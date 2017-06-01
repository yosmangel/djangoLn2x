from django import template

register = template.Library()

@register.filter
def colums_values(obj, elemnb):
    return obj.get_colums_values(elemnb)


