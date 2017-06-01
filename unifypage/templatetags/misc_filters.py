from django import template
from tldextract import extract

register = template.Library()

@register.filter('first_half')
def first_half_filter(value):
    return value[:len(value)//2]

@register.filter('second_half')
def second_half_filter(value):
    return value[len(value)//2:]


@register.filter
def clean_url(url=''):
    ext = extract(url)
    return '.'.join(ext)

