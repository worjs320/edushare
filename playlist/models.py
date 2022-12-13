from django.conf import settings
from django.db import models
from django.utils import timezone

class Playlist(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    user_name = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200)
    thumnail_id = models.CharField(max_length=100, default='', null=True)
    youtube_ids = models.CharField(max_length=1000, default='', null=True)
    youtube_ids_count = models.IntegerField(null=True)
    description = models.TextField()
    view_count = models.IntegerField()
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='playlist_like_count', blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()

class PlaylistNote(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    user_name = models.CharField(max_length=200, null=True)
    title = models.TextField(null=True)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
