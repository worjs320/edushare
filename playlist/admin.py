from django.contrib import admin
from .models import Playlist
from .models import PlaylistNote

admin.site.register(Playlist)
admin.site.register(PlaylistNote)