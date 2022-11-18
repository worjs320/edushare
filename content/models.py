from django.conf import settings
from django.db import models
from django.utils import timezone


class Content(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200)
    youtube_link = models.CharField(max_length=200)
    youtube_thumbnail = models.CharField(max_length=200, default='')
    youtube_code = models.CharField(max_length=200, default='', null=True)
    description = models.TextField()
    view_count = models.IntegerField()
    like_count = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
