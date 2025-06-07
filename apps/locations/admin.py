from django.contrib import admin
from .models import Country, Province, City, CustomLocation

# Register your models here.
admin.site.register(Country)
admin.site.register(Province)
admin.site.register(City)
admin.site.register(CustomLocation)

