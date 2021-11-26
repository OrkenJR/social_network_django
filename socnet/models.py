from enum import Enum

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib.humanize.templatetags import humanize


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_avatar', default='user_avatar/person.png')
    quote = models.CharField(max_length=150)
    birth_date = models.DateTimeField(blank=True, null=True)


class Post(models.Model):
    body = models.TextField()
    image = models.ImageField(upload_to='posts', blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(User, related_name='dislikes', blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def get_likes(self):
        return self.likes.count() - self.dislikes.count()

    def __str__(self):
        return self.body


class Comments(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)

    def calculate_days_ago(self):
        return humanize.naturaltime(self.created)

    def __str__(self):
        return 'Comment by {}'.format(self.user.username)
