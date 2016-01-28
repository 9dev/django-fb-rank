from django import template

from .. import utils


register = template.Library()


@register.simple_tag
def get_rank(obj):
    return utils.get_rank(obj)
