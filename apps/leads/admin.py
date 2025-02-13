from django.contrib import admin
from .models import Lead, ActivityTimeline, Note

# Register your models here.
admin.site.register(Lead)
admin.site.register(ActivityTimeline)
admin.site.register(Note)