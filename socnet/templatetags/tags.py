from django import template

register = template.Library()


@register.filter
def have_parents(things):
    return things.filter(parent__isnull=True)

