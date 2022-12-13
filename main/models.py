from django.db import models
from django.conf import settings

# 썸네일 저장
from django.core.files import File
import urllib.request
import os


# Create your models here.
class Song(models.Model):
    vidid = models.CharField(max_length=130, default=None, null=True)
    title = models.CharField(max_length=150, default=None, null=True)
    channel = models.CharField(max_length=130, default=None, null=True)
    default = models.CharField(max_length=130, default=None, null=True)
    mqdefault = models.CharField(max_length=130, default=None, null=True)
    hqdefault = models.CharField(max_length=130, default=None, null=True)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_song"
    )

    def __str__(self):
        return self.title
