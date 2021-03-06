from enum import Enum

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_avatar', default='user_avatar/person.png')
    quote = models.CharField(max_length=150)
    birth_date = models.DateTimeField()


class Post(models.Model):
    body = models.TextField()
    image = models.ImageField(upload_to='posts')
    date_posted = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='likes')
    dislikes = models.ManyToManyField(User, related_name='dislikes')

    def __str__(self):
        return self.body
