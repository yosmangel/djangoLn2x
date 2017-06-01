from django import template
from unifypage.models import UnifyPage, Element
from mezzanine.core.models import CONTENT_STATUS_PUBLISHED

register = template.Library()

@register.filter
def related_stuff(element, unifypage):
    if '-related-' in element.title:
        result = Element()
        pos = int(element.content)
        children = unifypage.children.order_by("_order")
        if children.count() >= pos:
            child = children[pos-1].unifypage
            result.title = child.title
            result.content = child.intro
            result.more_url = '/' + child.slug
            result.icon_url = child.image_url
        else:
            result.title = 'title test'
            result.content = 'content test'
            result.more_url = 'more_url test'
        return result
    else:
        return element
