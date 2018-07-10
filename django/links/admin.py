from django.contrib import admin
from .models import ShortURL, Viewer

admin.site.register(ShortURL)
admin.site.register(Viewer)
