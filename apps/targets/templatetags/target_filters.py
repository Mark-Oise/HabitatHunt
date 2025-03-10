from django import template
from apps.targets.models import Target

register = template.Library()

@register.filter
def filter_by_platform(targets, platform_id):
    """Filter targets by platform id"""
    return [target for target in targets if target.platform.id == platform_id]

