from django.template.loader import get_template
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def unify_form(context, formelement, template="unifypage/form.html"):
    """
    Renders a form with an optional template choice.
    """
    context["formelement"] = formelement
    return get_template(template).render(context)

