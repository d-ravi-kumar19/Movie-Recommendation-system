# recommend/admin.py
from django.contrib import admin
from .models import *

# Register your models here.
class RecommendAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'cast', 'director')  
    
admin.site.register(Movies, RecommendAdmin)
admin.site.register(Metadata)
admin.site.register(UserCredentials)
admin.site.register(UserTracking)