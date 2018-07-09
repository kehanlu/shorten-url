from django.db import models
from django.utils import timezone


class ShortURL(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=200, blank=True)
    target = models.CharField(max_length=200)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(upload_to='thumbnails/%m/', blank=True)
    permanent_url = models.CharField(max_length=20, blank=True)
    count = models.IntegerField(default=0)
    mode = models.IntegerField(default=301)

    def __str__(self):
        return self.permanent_url


class Viewer(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    short_url = models.ForeignKey(
        ShortURL, on_delete=models.CASCADE, related_name='viewers')
    ip = models.CharField(max_length=100)

    def __str__(self):
        return '{} - {}'.format(self.short_url.permanent_url, self.ip)
