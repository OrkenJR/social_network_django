from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Post(models.Model):
    body = models.TextField()
    image = models.ImageField(upload_to='posts', default='posts/default.jpg')
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.body
