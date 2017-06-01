from django import template

register = template.Library()

@register.filter
def testimonial_block(obj, lang):
    return obj.get_testimonial_block(lang)

