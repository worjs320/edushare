from django.conf import settings
from django.db import models
from django.utils import timezone


class Content(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    user_name = models.CharField(max_length=200, null=True)
    title = models.CharField(max_length=200)
    youtube_id = models.CharField(max_length=200, default='', null=True)
    description = models.TextField()
    view_count = models.IntegerField()
    like_count = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.save()

class Note(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    user_name = models.CharField(max_length=200, null=True)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.content.title + '에 대한 댓글'
