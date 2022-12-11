from django.db import models

# Create your models here.
class Song(models.Model):
    vidid = models.CharField(max_length=130, default=None, null=True)
    title = models.CharField(max_length=150, default=None, null=True)
    channel = models.CharField(max_length=130, default=None, null=True)
    default = models.CharField(max_length=130, default=None, null=True)
    mqdefault = models.CharField(max_length=130, default=None, null=True)
    hqdefault = models.CharField(max_length=130, default=None, null=True)
    hqdefault = models.CharField(max_length=130, default=None, null=True)

    def __str__(self):
        return self.title
