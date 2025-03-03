from django import template
from apps.leads.models import Lead

register = template.Library()

@register.filter
def filter_by_platform(leads, platform_id):
    """Filter leads by platform id"""
    return [lead for lead in leads if lead.source and lead.source.id == platform_id]

@register.filter
def filter_by_status(leads, status):
    return [lead for lead in leads if lead.status == status]