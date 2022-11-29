from django.contrib import admin
from .models import Content
from .models import Note

admin.site.register(Content)
admin.site.register(Note)