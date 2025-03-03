from django.contrib import admin
from .models import User, Realtor, RealtorPreference
from .forms import RealtorPreferenceForm

# Register your models here.
admin.site.register(User)
admin.site.register(Realtor)


@admin.register(RealtorPreference)
class RealtorPreferenceAdmin(admin.ModelAdmin):
    form = RealtorPreferenceForm