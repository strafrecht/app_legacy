from django import template
from pages.models import Sidebar

register = template.Library()

@register.inclusion_tag('pages/tags/sidebars.html', takes_context=True)
def sidebars(context):
    return {
        'sidebars': Sidebar.objects.all(),
        'request': context['request'],
    }
