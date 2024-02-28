from django.contrib import admin
from .models import *

# Register your models here.
class recommendAdmin(admin.ModelAdmin):
    list_display = ('movie','cast','director')

admin.site.register(Movies)
admin.site.register(Credits,recommendAdmin)
admin.site.register(Metadata)
admin.site.register(UserCredentials)
admin.site.register(UserTracking)
