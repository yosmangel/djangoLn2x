from django import template

from mezzanine.blog.models import BlogPost

register = template.Library()

@register.simple_tag()
def last_blogposts(x=1):
    """
    returns the x last blogposts
    """
    if isinstance(x, str):
        x = int(x)
    return BlogPost.objects.published()[:x]
