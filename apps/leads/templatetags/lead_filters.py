from django import template
from apps.leads.models import Lead

register = template.Library()

@register.filter
def filter_by_platform(leads, platform):
    return [lead for lead in leads if lead.source == platform]

@register.filter
def filter_by_status(leads, status):
    return [lead for lead in leads if lead.status == status]