from django.contrib import admin
from .models import Lead, LeadPreference, ActivityTimeline, Note, RawComment

class LeadPreferenceAdmin(admin.ModelAdmin):
    filter_horizontal = ('platforms', 'hashtags', 'targets')  # Use filter_horizontal for better M2M UI
    list_display = ('user', 'engagement_threshold', 'default_frequency')

# Register your models here
admin.site.register(Lead)
admin.site.register(LeadPreference, LeadPreferenceAdmin)
admin.site.register(ActivityTimeline)
admin.site.register(Note)
admin.site.register(RawComment)