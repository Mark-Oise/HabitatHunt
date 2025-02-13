from django import template

register = template.Library()

@register.filter
def filter_by_platform(leads, platform):
    return [lead for lead in leads if lead.source == platform]