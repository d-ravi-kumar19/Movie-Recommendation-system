from django.contrib import admin

# Register your models here.
from .models import Movies, Credits

admin.site.register(Movies)
admin.site.register(Credits)