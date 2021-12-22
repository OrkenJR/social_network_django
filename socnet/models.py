from enum import Enum

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.contrib.humanize.templatetags import humanize


class Chat(models.Model):
    participants = models.ManyToManyField(User, related_name='chats')
    created = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat')
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=250)


class Group(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name="admin")
    image = models.ImageField(upload_to='group_img', default='group/vk-logo.png')
    name = models.CharField(max_length=150)
    followers = models.ManyToManyField(User, blank=True, related_name="followers")


class FriendList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(User, blank=True, related_name="friends")

    def add_friend(self, user):
        if not user in self.friends.all():
            self.friends.add(user)
            self.save()

    def remove_friend(self, user):
        if user in self.friends.all():
            self.friends.remove(user)

    def unfriend(self, delete_user):
        friend_list = self
        friend_list.remove_friend(delete_user)
        deleting_friend_list = FriendList.objects.get(user=delete_user)
        deleting_friend_list.remove_friend(self.user)


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    is_active = models.BooleanField(blank=True, null=False, default=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def accept(self):
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)

            try:
                sender_friend_list = FriendList.objects.get(user=self.sender)
            except FriendList.DoesNotExist:
                sender_friend_list = FriendList(user=self.sender)
                sender_friend_list.save()

            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        self.is_active = False
        self.save()

    def cancel(self):
        self.is_active = False
        self.save()


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
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True)
    group_author = models.ForeignKey(Group, on_delete=models.CASCADE, default=None, null=True, blank=True)

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
