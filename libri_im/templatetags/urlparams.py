from django import template
from django.utils.http import urlencode

register = template.Library()
'''This function takes the url and replaces the url'''
@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)
    return urlencode(query)
