from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    place = models.CharField(max_length=30)
    song = models.CharField(max_length=30)
    singer = models.CharField(max_length=30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = ProcessedImageField(
        upload_to="images/",
        blank=True,
        processors=[ResizeToFill(400, 300)],
        format="JPEG",
        options={"quality": 90},
    )
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_article"
    )


class Place(models.Model):
    name = models.TextField()
    # user를 foreignKey로 가져와야한다.


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Likesong(models.Model):
    like = models.ForeignKey(Like, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
